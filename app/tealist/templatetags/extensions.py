from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor

# https://www.mattlayman.com/blog/2023/python-markdown-tailwind-best-buds/


class TailwindExtension(Extension):
    """An extension to add classes to tags"""

    def extendMarkdown(self, md):
        md.treeprocessors.register(TailwindTreeProcessor(md), "tailwind", 20)


class TailwindTreeProcessor(Treeprocessor):
    """Walk the root node and modify any discovered tag"""

    classes = {
        "h1": "font-serif font-bold text-4xl",
        "h2": "font-serif font-bold text-3xl text-secondary",
        "h3": "font-serif font-bold text-2xl",
        "h4": "font-serif font-bold text-1xl text-secondary",
        "h5": "font-serif font-bold text-lg",
        "ul": "list-disc list-inside",
        "a": "text-secondary border-b border-transparent hover:border-b hover:border-secondary transition ease-in-out",
    }

    def run(self, root):
        for node in root.iter():
            tag_classes = self.classes.get(node.tag)
            if tag_classes:
                node.attrib["class"] = tag_classes
