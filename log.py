import inspect, time, sys

class Log:
    prefix : str
    def __init__(self, prefix = "") -> None:
        self.prefix = prefix

    def getStrTime(self):
        return time.strftime('[%m.%d %H:%M:%S]')

    def log(self, *args, createfile=False, isCrash=False, **kwargs):
        text = ""
        for v in args: text += "{}\t".format(v)
        if kwargs:
            for k in kwargs: text += "{} = {}\t".format(k, kwargs[k])
        text = text[:-1]

        frame = inspect.getouterframes(inspect.currentframe())[1]
        text = f"{self.getStrTime()} {self.prefix} ({frame.function}:{frame.lineno}): "+text

        if isCrash:
            text += f"\nSTACK TRACE:\n"
            trace = inspect.trace()
            i = 0
            for frame in trace:
                context = ''.join(frame.code_context).replace('\n', '')
                if i == len(trace)-1:
                    context = context[:frame.positions.col_offset] + '>>' + context[frame.positions.col_offset:]
                    text += f"{frame.function}({frame.lineno}:{frame.positions.col_offset}){context}\n"
                else:
                    text += f"{frame.function}({frame.lineno}){context}\n"
                i+=1
        if "-dev" in sys.argv or '-log' in sys.argv:
            print(text)
        if createfile:
            open("log.txt", "w")
        open("log.txt", 'a', encoding="utf-8").write(text+"\n")