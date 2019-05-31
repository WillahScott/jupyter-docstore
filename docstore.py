from IPython.core.magic import Magics, magics_class, cell_magic, line_magic
from IPython.display import Latex, display
from pprint import pprint


DEFAULT_DOC = 'latex_from_ipynb.tex'


@magics_class
class TexDocSaver(Magics):

    def __init__(self, shell=None,  **kwargs):
        super().__init__(shell=shell, **kwargs)
        # the store will have one item per tex file
        self._store = {}
        # inject our store in user available namespace under __mystore
        # name
        shell.user_ns['__mystore'] = self._store

    @cell_magic
    def preview_tex(self, line, cell):
        """store the cell in the store"""
        print('This is just a preview, to store use `%%save_tex {doc_name}`')
        # display LaTeX
        print('=== LaTeX Preview ===')
        display(Latex(cell))

    @cell_magic
    def save_tex(self, line, cell):
        """store the cell in the store"""
        # if no document was specified, save to DEFAULT_DOC
        texdoc = line if line != '' else DEFAULT_DOC
            
        print(f'Storing cell contents to document: {texdoc}')
        self._store[texdoc] = self._store.get(texdoc, []) + [cell]

        # display LaTeX
        print('=== LaTeX Preview ===')
        display(Latex(cell))

        
    def _write(self, doc):
        """Write the specified document to disk"""
        # merge cells together into a single string
        docstream = ''.join(self._store[doc])

        print(f'Writing document: {doc}')
        with open(doc, 'w') as f:
            f.write(docstream)

            
    @line_magic
    def dump_tex(self, line):
        """Dump the cell content into the physical document"""
        if line != '':
            if line not in self._store:
                raise ValueError(f'No such doc ({line}) found in the store')
            else:
                self._write(line)
        else:
            self.dump_all_docs('')

            
    @line_magic
    def dump_all_docs(self, line):
        """Dump all th cell data into the physical documents"""
        for doc in self._store.keys():
            self._write(doc)

            
    @line_magic
    def show_saved(self, line):
        """Show all recorded documents and their cells"""
        pprint(self._store)
