from langchain.text_splitter import MarkdownHeaderTextSplitter
import tiktoken
import matplotlib.pyplot as plt

def split_text( docs):
    headers_to_split_on = [
        ("#", "H1"),
        ("##", "H2"),
        ("###", "H3"),
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    fragments =[]
    for ix, text in enumerate(docs):
        items = markdown_splitter.split_text(text)
        for i in items:
            s=""
            if "H3" in i.metadata:
                s = i.metadata["H3"]+"\n"+ s
            if "H2" in i.metadata:
                s = i.metadata["H2"]+"\n"+ s
            if "H1" in i.metadata:
                s = i.metadata["H1"]+"\n"+ s
            if s:
                i.page_content = s+ i.page_content
            i.metadata["ix"]=ix
        fragments.extend( items)
    return fragments


def num_tokens_from_string( string: str, encoding_name: str= "cl100k_base") -> int:
    """Возвращает количество токенов в строке"""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def hist(fragments):
    fragment_token_counts = [num_tokens_from_string(fragment.page_content, "cl100k_base") for fragment in fragments]
    plt.hist(fragment_token_counts, bins=20, alpha=0.5, label='Fragments')
    plt.title('Distribution of Fragment Token Counts')
    plt.xlabel('Token Count')
    plt.ylabel('Frequency')
    plt.show()


