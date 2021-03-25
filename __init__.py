import os
import re
import json
from cudatext import *
#from cudax_lib import get_translation

#_   = get_translation(__file__)  # I18N

""" file:///install.inf
"""

fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_hot_nest.json')

CMDS = {
    'hot--lsp':{
        'regex_0_target': 'p_caption',
        'regex_0': r'^_LSP\\[^\\]+$', # direct children
    },
    'hot--Sort':{
        'regex_0_target': 'p_caption',
        'regex_0': r'^Sort\\.*(Sort,|shuffle|reverse|blank)',
    }
}
    
option_add_ind = True

class Command:
    
    def __init__(self):
        self.keys = app_proc(PROC_GET_COMMANDS, '')
        self.h_menu = None

        self.load_config()
        
        if CMDS:
            subcmds = '\n'.join('{}\t{}'.format(name, name)  for name in CMDS)
            app_proc(PROC_SET_SUBCOMMANDS, 'cuda_hot_nest;show_mmenu;'+subcmds)

    def config(self):
        if not os.path.exists(fn_config):
            cfg = {'add_indexes': option_add_ind, 'menus': CMDS}
            with open(fn_config, 'w', encoding='utf-8') as f:
                json.dump(cfg, f, indent=2)
        file_open(fn_config)
        
    def load_config(self):
        global option_add_ind
        
        if os.path.exists(fn_config):
            with open(fn_config, 'r', encoding='utf-8') as f:
                j = json.load(f)
                
            option_add_ind = j.get('add_indexes', option_add_ind)
            
            if 'menus' in j:
                CMDS.clear()
                CMDS.update(j['menus'])
        
    def on_start(self, ed_self):
        pass
        
    def show_mmenu(self, name):
        if name not in CMDS:
            print(' -- no such menu-comamnd: ', name)
            return
        
        if not self.h_menu:
            h_menu = menu_proc(0, MENU_CREATE)
            
        items = filter_items(self.keys, CMDS[name])
        if not items:
            print('no items ...')
            return
        if len(items) > 15:
            print('toomany items:', len(items))
            del items[16:]

        menu_proc(h_menu, MENU_CLEAR)
        
        for i,item in enumerate(items):
            cap = item.get('p_caption', '').replace('&', '').split('\\')[-1]  or  item.get('name', '<noname>')
            if option_add_ind:
                cap = '&{} {}'.format(i+1, cap)
            menu_proc(h_menu, MENU_ADD, command=item['cmd'], caption=cap)
        
        menu_proc(h_menu, MENU_SHOW)
        
    def view_keys(self):
        cmds = app_proc(PROC_GET_COMMANDS, '')
        file_open('')
        ed.set_text_all(json.dumps(cmds, indent=2))
        ed.set_prop(PROP_LEXER_FILE, 'JSON')
        

def filter_items(keys, d):
    for i in range(16):
        key = 'regex_'+str(i)
        regex,target = d.get(key), d.get(key+'_target')
        if not regex or not target:
            break
        
        keys = [key for key in keys  if re.match(regex, key.get(target, ''))]
    return keys
        