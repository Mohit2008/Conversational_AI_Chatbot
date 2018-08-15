import os
import sys  # NOQA
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir, os.pardir))
from cmd2 import Cmd, options, make_option
from searchEngine.indexer.index import get_all_txt_files,create_index, update_existing_index, create_fresh_index, update_indexed_document
from searchEngine.searcher.search import do_search
from searchEngine.seconfig import SearchEngineConfig
from searchEngine.system.sysinfo import get_os_hardware_information
from searchEngine.system.sysinfo import get_interpreter_information
from searchEngine.system.sysinfo import get_platform_information

#  All the shell intercativity for the search engine are defined here
class InteractiveCommands(Cmd):
    @options([make_option('-d', '--dir', type=str, help="DIRECTORY")])
    def do_set_search_directory(self, args, opts):
        if not (opts.dir):
            raise Exception('please specify a directory to search in')
        else:
            SearchEngineConfig.DOCUMENT_LOOKUP_DIRECTORY=opts.dir
            print("Success")

    def do_create_index(self, args):
        """Initial pre requisite step to start up the process of searching"""
        create_index()
        print("Success")

    @options([make_option('-q', '--query', type=str, help="QUERY")])
    def do_search(self, args, opts):
        """ Perform searching on indexed files"""
        if not (opts.query):
            raise Exception('please give a search query')
        do_search(opts.query)

    def do_get_system_properties(self, args):
        """ Know your system"""
        get_os_hardware_information()
        get_interpreter_information()
        get_platform_information()

    def do_update_index(self, args):
        """ Update the existing index with updated information"""
        update_existing_index()

    def do_create_fresh_index(self, args):
        """ Clear the existing index and create a new one"""
        create_fresh_index()

    @options([make_option('-p', '--path', type=str, help="PATH")])
    def do_update_indexed_document(self, args, opts):
        """ Update a document that is already indexed"""
        if not (opts.path):
            raise Exception('please give the path of the file to be updated')
        update_indexed_document(opts.path)


    def do_sehelp(self, args):
        print("""CLI provides the functionality of triggering the commands

==== Create Index

The command is  \t create_index

==== Do Searching

The command is  \t search -q some text

==== Set up the directory

The command is  \t set_search_directory -d "/path/"

==== Know your system

The command is  \t get_system_properties

==== Update the existing index with new added files and old removed files

The command is  \t update_index

==== Clear the existing index and create a new one

The command is  \t create_fresh_index

==== Update a document that is already indexed

The command is  \t update_indexed_document -p "/path/to/some/file"


==== Auto Completion feature

CLI comes with auto completion feature""")

    def help_se_shell(self):
        print("""***Welcome to the CLI for Search Engine utility commands! This is an online help utility.
the command sehelp() offers a short introduction***""")

    def do_quit(self, args):
        """Quits the program."""
        print("Quitting.")
        quit()

    def preloop(self):
        self.help_se_shell()

def init_commands():
    prompt = InteractiveCommands()
    prompt.prompt = 'Search Engine cli> '
    prompt.cmdloop()
