import re

file_name ="e:/Video/AResh/2023/NU_Stag/Gavrilov_stag/Статьи с Telegram.txt"


class TelegramPosts:
    def __init__(self, file_name):
        with open(file_name,"r", encoding="utf-8") as f:
            self.text = f.read()
        self.ar = self.text.split("\n")
        ar = self.ar
        if ar[0][:1]=='\ufeff':
            ar[0]=ar[0][1:]
        self.i_done = 0
    def read_contents(self):
        i_done=0
        self.contents = []
        for i, s in enumerate(self.ar):
            num:str = s[-4:].strip()
            if num.isnumeric():
                i_done = i
                n = int(num)
                item = (s[:-4].strip(),n)
                #print(item)
                self.contents.append(item)
            else:
                break
        self.i_done = i_done
        def f(s):
            m = re.search(r'Посты за (\d{4}) год',s[0])
            return m
        self.r = list(filter(f,self.contents))

    def base_parsing(self):
        ar = self.ar
        contents = self.contents
        i_done = self.i_done
        ar_t = ar[i_done + 1:]
        self.text = []
        text = self.text
        is_h = True
        is_h2 = False
        h = "##_"
        rl = [x[0] for x in self.r]
        i_contents = 1
        cont = [s[0] for s in contents]
        c = cont[i_contents]
        r2 = 0
        h2 = ""
        if c in rl:
            i_contents += 1
            c = cont[i_contents]
        for i, s in enumerate(ar_t):
            s = s.strip()
            found = False
            if s in cont[i_contents:]:
                j = cont[i_contents:].index(s)
                if j < 4:
                    i_contents += j + 1
                    is_h1 = False
                    is_h2 = False
                    pre = ""
                    if h2 == s:
                        r2 += 1
                        pre = f"{r2 + 1}. "
                    else:
                        r2 = 0
                        h2 = s
                    text.append("\n## " + pre + s)

                    # print(s)
                    found = True
                    if i_contents < len(contents):
                        c = contents[i_contents]
                    if c in rl:
                        i_contents += 1
                        c = contents[i_contents]
            if found:
                pass
            elif s == c[0]:
                is_h1 = False
                is_h2 = False
                pre = ""
                if h2 == s:
                    r2 += 1
                    pre = f"{r2 + 1}. "
                else:
                    r2 = 0
                    h2 = s
                text.append("\n## " + pre + s)
                # print(s)
                i_contents += 1
                if i_contents < len(contents):
                    c = contents[i_contents]
                if c[0] in rl:
                    i_contents += 1
                    c = contents[i_contents]
            elif s == "":
                is_h = True
            elif s == h:
                is_h2 = True
                is_h = False
            elif is_h:
                pre = ""
                if s in rl:
                    # print(s)
                    pre = "\n# "
                text.append(pre + s)
                is_h = False
            else:
                is_h = False
                if is_h2:
                    is_h2 = False
                    text.append("\n## " + s)
                else:
                    if s.startswith("#"):
                        s = f"#" + s[1:].strip()
                    text.append(s)

    def save(self):
        with open("out.md", "w", encoding="utf-8") as f:
            f.write("\n".join(self.text))


if __name__=="__main__":
    tp = TelegramPosts(file_name)
    tp.read_contents()
    tp.base_parsing()
    tp.save()
