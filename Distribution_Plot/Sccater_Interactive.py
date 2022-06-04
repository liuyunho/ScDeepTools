from __future__ import print_function
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection, PolyCollection, LineCollection
from collections import Counter, defaultdict, OrderedDict
from matplotlib.widgets import RectangleSelector
from matplotlib.path import Path
from matplotlib import widgets
from matplotlib.widgets import TextBox

class Distribution_Display(object):
    def __init__(self, ax, point_group, color_dict):
        self.collection={lab:None for lab in point_group}
        self.initialize_display(ax, point_group, color_dict)

    def initialize_display(self,ax, point_group, color_dict):
        for lab in point_group:
            self.collection[lab]=ax.scatter(point_group[lab]['x'],point_group[lab]['y'],s=5,c=color_dict[lab],picker=True)

class PickControl:
    def __init__(self, fig):
        self.fig = fig
        self._pickers = []
        self._pickcids = []
        
    def connect_picks(self):
        for i, picker in enumerate(self._pickers):
            if self._pickcids[i] is None:
                cid = self.fig.canvas.mpl_connect('pick_event', picker)
                self._pickcids[i] = cid
                
    def disconnect_picks(self):
        for i, cid in enumerate(self._pickcids):
            if cid is not None:
                self.fig.canvas.mpl_disconnect(cid)
                self._pickcids[i] = None

    def add_pick_action(self, picker):
        if not callable(picker):
            raise ValueError("Invalid picker. Picker function is not callable")
        if  picker in self._pickers:
            raise ValueError("Picker is already in the list of pickers")
        self._pickers.append(picker)
        cid = self.fig.canvas.mpl_connect('pick_event', picker)
        self._pickcids.append(cid)

class KeymapControl:
    def __init__(self, fig):
        self.fig = fig
        # Deactivate the default keymap
        #fig.canvas.mpl_disconnect(fig.canvas.manager.key_press_handler_id)
        self._keymap = OrderedDict()
        # Activate my keymap
        self.connect_keymap()
        self._lastkey = None

    def connect_keymap(self):
        self._keycid = self.fig.canvas.mpl_connect('key_press_event',
                                                   self.keypress)

    def disconnect_keymap(self):
        if self._keycid is not None:
            self.fig.canvas.mpl_disconnect(self._keycid)
            self._keycid = None

    def add_key_action(self, key, description, action_func):
        if not callable(action_func):
            raise ValueError("Invalid key action. Key '%s' Description '%s'"
                             " - action function is not a callable" %
                             (key, description))
        if key in self._keymap:
            raise ValueError("Key '%s' is already in the keymap" % key)
        self._keymap[key] = (description, action_func)

    def keypress(self, event):
        action_tuple = self._keymap.get(event.key, None)
        if action_tuple:
            self._lastkey = event.key
            action_tuple[1]()

    def display_help_menu(self):
        print("Help Menu")
        print("Key         Action")
        print("=========== ============================================")
        for key, (description, _) in self._keymap.items():
            print("%11s %s" % (key, description))

class ButtonControl:
    def __init__(self, fig, width, height):
        self.fig = fig
        # Give us some room along the top
        fig.subplots_adjust(top=1-height*2)
        self._buttonwidth = width
        self._buttonheight = height
        self._buttonmap = {}

    def connect_buttonmap(self):
        for text, (cid, func, button) in self._buttonmap.items():
            if cid is None:
                cid = button.on_clicked(func)
                self._buttonmap[text] = (cid, func, button)

    def disconnect_buttonmap(self):
        for text, (cid, func, button) in self._buttonmap.items():
            if cid is not None:
                button.disconnect(cid)
                self._buttonmap[text] = (None, func, button)

    def add_button_action(self, text, action_func):
        if not callable(action_func):
            raise ValueError("Invalid button action. Button '%s''s"
                             " action function is not a callable" % text)
        if text in self._buttonmap:
            raise ValueError("Button '%s' is already a button" % text)
        ax = self.fig.add_axes([len(self._buttonmap) * self._buttonwidth,
                                0.99 - self._buttonheight,
                                self._buttonwidth, self._buttonheight])
        button = widgets.Button(ax, text)
        # Swallow the event parameter. We don't need it for these buttons
        func = lambda event: action_func()
        cid = button.on_clicked(func)
        self._buttonmap[text] = (cid, func, button)

class ControlSys(PickControl, KeymapControl, ButtonControl):
    def __init__(self, fig, ax, SingleCell, Collection, Color_dic):
        self.fig = fig
        self.ax=ax
        self.singlecell = SingleCell
        self.collections = Collection
        self.selected = {lab:[] for lab in Collection}
        self.RS=None
        self._toggle_buttons = self.build_check_buttons(fig, 0.15)
        self._mode_buttons = self.build_radio_buttons(fig, 0.1)
        self.toggle_item={lab:True for lab in Collection}
        self._mode = 'Subtraction'
        self._save_index=1
        self._export_index=1
        self.delete_record=[]
        
        PickControl.__init__(self, fig)
        KeymapControl.__init__(self, fig)
        ButtonControl.__init__(self, fig, 0.08, 0.05)
        
        self._toggle_buttons.on_clicked(self.group_visibility)
        self._mode_buttons.on_clicked(self.set_mode)
        self._connect('select', self.highlight_cell)
        self._connect('delete', self.delete_cell)
        self._connect('help', lambda x: self.display_help_menu())
        
        self.add_key_action('d', 'Delete the selected cell',
                            self.delete_selected)
        self.add_key_action('t', 'Active rectangular selector',
                            self.toggle_selector)
        self.add_key_action('A', 'Addition mode',
                            lambda : self.set_mode('Addition'))
        self.add_key_action('S', 'Subtraction mode',
                            lambda : self.set_mode('Subtraction'))
        self.add_key_action('h', 'Display this help menu',
                            lambda : self._emit('help', None))
        
        self.add_pick_action(self.select_cell)
        
        self.add_button_action('Export(e)', self.export_select)
        self.add_button_action('Save(s)', self.save_data)
        self.add_button_action('Rect(t)', self.toggle_selector)
        self.add_button_action('Reset(r)', self.reset_select)
        self.add_button_action('Del(d)', self.delete_selected)
        self.add_button_action('Back(b)', self.back_delete)
        self.add_button_action('Add(A)', lambda : self.set_mode('Addition')) #add lambda make the function callable
        self.add_button_action('Sub(S)', lambda : self.set_mode('Subtraction'))
        self.add_button_action('Help(h)', lambda : self._emit('help', None))
        
        print('Your working directory is: '+os.getcwd(),end='\n')
        self._text_box = self.build_text_box(fig)
        self._text_box.on_text_change(self._textbox_cursor)
        self._text_box.on_submit(self.text_submit)
         
    def _emit(self, event, eventdata):
        self.fig.canvas.callbacks.process(event, eventdata)

    def _connect(self, event, callback):
        self.fig.canvas.mpl_connect(event, callback)
    
    #backward
    def back_delete(self):
        if len(self.delete_record)==0:
            return
        sub_delete=self.delete_record[0]
        del self.delete_record[0]
        #start add data
        self.add_data(sub_delete)
    
    def add_data(self,delete_part):
        for lab in delete_part:
            self.singlecell.group[lab]['x']+=delete_part[lab]['x']
            self.singlecell.group[lab]['y']+=delete_part[lab]['y']
            self.singlecell.group[lab]['identifer']+=delete_part[lab]['identifer']
            self.singlecell.group[lab]['index']+=delete_part[lab]['index']
            self.singlecell.group[lab]['label']+=delete_part[lab]['label']
            self.singlecell.group_len[lab]+=len(delete_part[lab]['x'])
            #reorder 先不用试试
            self.collections[lab].set_offsets(np.array([self.singlecell.group[lab]['x'],self.singlecell.group[lab]['y']]).T)
        
    #reset
    def reset_select(self):
        for lab in self.selected:
            if not self.toggle_item[lab]:
                continue
            self.selected[lab]=[]
        self.reset_color()
        
    #export
    def export_select(self):
        ids,d1,d2,la=[],[],[],[]
        for lab in self.selected:
            if not self.toggle_item[lab]:
                continue
            ids+=[self.singlecell.group[lab]['identifer'][i] for i in self.selected[lab]]
            d1+=[self.singlecell.group[lab]['x'][i] for i in self.selected[lab]]
            d2+=[self.singlecell.group[lab]['y'][i] for i in self.selected[lab]]
            la+=[self.singlecell.group[lab]['label'][i] for i in self.selected[lab]]
        new_data=pd.DataFrame({'Identifer':ids,
                    'Dimension 1':d1,
                    'Dimension 2':d2,
                    'Label':la})
        new_data.to_csv("Data_selected_"+str(self._export_index)+".csv",index=False,sep=',')
        self._export_index+=1
            
            
    #save
    def save_data(self):
        ids,d1,d2,la=[],[],[],[]
        for lab in self.singlecell.group:
            if not self.toggle_item[lab]:
                continue
            ids+=self.singlecell.group[lab]['identifer']
            d1+=self.singlecell.group[lab]['x']
            d2+=self.singlecell.group[lab]['y']
            la+=self.singlecell.group[lab]['label']
        new_data=pd.DataFrame({'Identifer':ids,
                    'Dimension 1':d1,
                    'Dimension 2':d2,
                    'Label':la})
        new_data.to_csv("Data_left_"+str(self._save_index)+".csv",index=False,sep=',')
        self._save_index+=1
        
    #text box
    def build_text_box(self, fig):
        # Give us some room along the right
        fig.subplots_adjust(bottom=0.2)
        axbox = fig.add_axes([0.2, 0.05, 0.6, 0.025])
        text_box = TextBox(axbox, 'Change your working directory:', initial=os.getcwd())
        return text_box
    
    def _textbox_cursor(self,tem):
        self.disconnect_keymap()
        
    def text_submit(self,text):
        self.connect_keymap()
        os.chdir(text)
        print('Your working directory is: '+os.getcwd(),end='\n')
    
    #check button
    def build_check_buttons(self, fig, width):
        # Give us some room along the right
        fig.subplots_adjust(right=1-width)
        boxax = fig.add_axes([1 - width, 0.6, width, 0.2])
        checks = widgets.CheckButtons(boxax, tuple(self.collections.keys()),
                                  [True]*len(self.collections))
        return checks
    
    def group_visibility(self,item):
        self.toggle_item[item] = not self.toggle_item[item]
        if self.toggle_item[item]:
            self.collections[item].set_color(self.singlecell.color_dict[item]) 
        else:
            self.collections[item].set_color('#EBEBEB') 
        self.selected[item]=[]
        self.fig.canvas.draw_idle()
    
    #radio button
    def build_radio_buttons(self, fig, height):
        # Give us some room along the top
        fig.subplots_adjust(top=1-height)
        button_ax = fig.add_axes([0.85, 1 - height, 0.14, height])
        buttons = widgets.RadioButtons(button_ax, ('Subtraction','Addition'))
        # Compatibility layer (this method was not added until v1.5)
        if not hasattr(buttons, 'set_active'):
            def set_active(index):
                if 0 > index >= len(buttons.labels):
                    raise ValueError("Invalid RadioButton index: %d" % index)

                for i, p in enumerate(buttons.circles):
                    if i == index:
                        color = buttons.activecolor
                    else:
                        color = buttons.ax.get_axis_bgcolor()
                    p.set_facecolor(color)

                if buttons.drawon:
                    buttons.ax.figure.canvas.draw()

                if not buttons.eventson:
                    return
                for cid, func in buttons.observers.items():
                    func(buttons.labels[index].get_text())
            buttons.set_active = set_active
        return buttons
    
    def set_mode(self, mode):
        if mode != self._mode:
            self._mode_buttons.eventson = False
            if mode == 'Addition':
                self._mode_buttons.set_active(1)
            elif mode == 'Subtraction':
                self._mode_buttons.set_active(0)
            else:
                self._mode_buttons.eventson = True
                raise ValueError("Invalid mode value: %s" % mode)
            self._mode_buttons.eventson = True
            self._mode = mode
        
    #high light and delete function
    def highlight_cell(self, selects, col='#FFFF00'):
        for lab in selects:
            if not self.toggle_item[lab]:
                continue
            if len(selects[lab]) > 0:
                color = [self.singlecell.group_col[lab]]*self.singlecell.group_len[lab]
                for j in selects[lab]:
                    color[j] = col
                self.collections[lab].set_color(color) 

    def delete_selected(self):
        self._emit('delete', self.selected)
        self.selected = {lab:[] for lab in self.collections}
        self.fig.canvas.draw_idle()
    
    def reset_color(self):
        for lab in self.collections:
            if not self.toggle_item[lab]:
                continue
            color = [self.singlecell.group_col[lab]]*self.singlecell.group_len[lab]
            self.collections[lab].set_color(color) 
    
    def delete_cell(self, selects):
        sub_delete= defaultdict(dict)
        for lab in selects:
            if not self.toggle_item[lab]:
                continue
            if len(selects[lab])>0:
                sub_delete[lab]['x'],sub_delete[lab]['y'],sub_delete[lab]['index'],sub_delete[lab]['identifer'],sub_delete[lab]['label']=[],[],[],[],[]
                shift_index=0
                for ind in sorted(selects[lab]):
                    sub_delete[lab]['x'].append(self.singlecell.group[lab]['x'][ind-shift_index])
                    del self.singlecell.group[lab]['x'][ind-shift_index]
                    sub_delete[lab]['y'].append(self.singlecell.group[lab]['y'][ind-shift_index])
                    del self.singlecell.group[lab]['y'][ind-shift_index]
                    sub_delete[lab]['index'].append(self.singlecell.group[lab]['index'][ind-shift_index])
                    del self.singlecell.group[lab]['index'][ind-shift_index]
                    sub_delete[lab]['identifer'].append(self.singlecell.group[lab]['identifer'][ind-shift_index])
                    del self.singlecell.group[lab]['identifer'][ind-shift_index]
                    sub_delete[lab]['label'].append(self.singlecell.group[lab]['label'][ind-shift_index])
                    del self.singlecell.group[lab]['label'][ind-shift_index]
                    self.singlecell.group_len[lab]-=1
                    shift_index+=1
                self.collections[lab].set_offsets(np.array([self.singlecell.group[lab]['x'],self.singlecell.group[lab]['y']]).T)
        self.delete_record.append(sub_delete)
        self.reset_color()
    
    #rectangular selector
    def toggle_selector(self):
        if not self.RS:
            print(' RectangleSelector activated and Pck deactivated')
            self.RS = RectangleSelector(self.ax, self.which_select,button=[1, 3],interactive=True,useblit=False)
            self.disconnect_picks()
            return
        if self.RS.active:
            print(' RectangleSelector deactivated and Pck activated')
            self.connect_picks()
            self.RS.set_active(False)
        else:
            print(' RectangleSelector activated and Pck deactivated')
            self.disconnect_picks()
            self.RS.set_active(True)
    
    def contains(self, x1, y1, x2, y2):
        min_x, max_x = min(x1, x2), max(x1, x2)
        min_y, max_y = min(y1, y2), max(y1, y2)
        return np.where(np.array(self.singlecell.x>min_x) & np.array(self.singlecell.x<max_x) & np.array(self.singlecell.y>min_y) & np.array(self.singlecell.y<max_y))
    
    # --- Selection/Deselection methods ---  
    def mode_choise(self,ind,lab):
        if self._mode=='Addition':
            if ind in self.selected[lab]:
                pass
            else:
                self.selected[lab].append(ind)
        elif self._mode=='Subtraction':
            if ind in self.selected[lab]:
                self.selected[lab].remove(ind)
            else:
                self.selected[lab].append(ind)

    #rectangular
    def which_select(self,evnt_click, evnt_release):
        self.where = self.contains(evnt_click.xdata, evnt_click.ydata,evnt_release.xdata, evnt_release.ydata)
        for ind_a in self.where[0]:
            for lab in self.singlecell.group:
                if ind_a in self.singlecell.group[lab]['index']:
                    ind=self.singlecell.group[lab]['index'].index(ind_a)
                    self.mode_choise(ind,lab)
                    break
        self._emit('select', self.selected)
        self.fig.canvas.draw_idle()
        
    #picker 
    def select_cell(self, event):
        inds = event.ind
        for lab in self.collections:
            if not self.toggle_item[lab]:
                continue
            if event.artist==self.collections[lab]:
                for ind in inds:
                    self.mode_choise(ind,lab)
                break
        self._emit('select', self.selected)
        self.fig.canvas.draw_idle()