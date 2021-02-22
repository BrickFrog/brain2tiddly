import sys
import os
import pathlib
import time
import re
from datetime import datetime
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class ObsidianNote:
    '''Class representing a note in Obsidian. 
    This generally implies nested folders and markdown.'''
    # TODO: Implement this in future, keeping as a reminder
    title: str
    tags: List[str]
    created: datetime
    modified: datetime
    body: str

@dataclass
class TiddlyNote:
    '''Class representing a TiddlyWiki tiddler'''
    title: str
    created: str
    modified: str
    tags: str
    body: str
        

    def parse(self):
        
        # TODO - this is stripping off last 3 chars as .md, might not
        # be as relevant once introducing new filetypes
        name = self.title[:-3]
        filename = f'tiddlers/{name}.tid'
        
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc: # Guard against race condition
                if exc.errno != exc.errno.EEXIST:
                    raise

        with open(filename, 'w') as f:
            f.write(f'created: {self.created}\n')
            f.write(f'modified: {self.modified}\n')
            f.write(f'tags: {self.tags}\n')
            f.write(f'title: {name}\n')
            f.write(f'\n{self.body}')

def list_files(dir: str) -> List:
    r = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            filepath = root + os.sep + name
            
            if filepath.endswith(".md") and 'Assets' not in filepath:
                file_path = pathlib.Path(os.path.join(root, name))
                file_stats = file_path.stat()
                create_time = datetime.fromtimestamp(file_stats.st_ctime) 
                mod_time = datetime.fromtimestamp(file_stats.st_mtime)
                
                parts = []
                for part in file_path.parts:
                    if part not in pathlib.Path(dir).parts:
                        parts.append(part)
                
                r.append([filepath, parts, create_time, mod_time])
    return r

def header_repl(m) -> str:
    '''markdown # symbols for headers are 
    denoted by !'s in tiddlywiki'''
    return '!' * len(m.group())

def thoughts_header_repl(m) -> str:
    '''I use a custom header for journal entries
    in the format of [[a | b]] | [[a | b]], the way
    that links are handled in TW requires b | a'''
    text = m.group()
    try:
        text_list = text[2:-2].split('|')
        return '[[' + text_list.reversed() + ']]'
    except:
        return text

def subject_repl(m) -> str:
    '''replaces the extranous parts of a link, since tiddlywiki
    doesn't make use of folders like obsidian does'''
    return '[['

def tag_return(file) -> List:
    '''removes tags from file, returning them upwards'''
    matches = re.findall('Y[\d\s]\d*\w\d{2}', file)
    file = re.sub('Tags.*\n', '', file)
    return matches, file

def file_parser(listed_files: List):
    
    for group in listed_files:
    
        with open(group[0]) as f:
            # TODO: probably a better way to handle this
            file = f.read()
            file = re.sub('^#+', header_repl, file, flags = re.MULTILINE)
            file = re.sub('\[[^\]]*\]]', thoughts_header_repl, file, flags = re.MULTILINE)
            file = re.sub('\[\[(\w+\/){1,}', subject_repl, file, flags = re.MULTILINE)
            
            tags, file = tag_return(file)
            
        # TODO: Definitely a better way to handle this
        tags = ", ".join(tags).replace("Y","").replace("M","")
            
        if len(tags) != 0:
            tags = tags + ", "
        else:
            tags
            
            
        tiddler = TiddlyNote(
            title = group[1].pop(),
            created = group[2].strftime('%Y%m%d%H%M%S000'),
            modified = group[3].strftime('%Y%m%d%H%M%S000'),
            tags = (tags + ", ".join(group[1])).replace(",", ""),
            body = file
        )
        
        tiddler.parse()

if __name__ == "__main__":
    # End goal would be to turn this into a CLI
    file_parser(list_files('vault'))