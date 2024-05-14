import framebuf

class MyBuffer2D:
    
    def __init__(self,inx: int,iny: int):
        self.buffer = bytearray(inx * iny)
        self.nx = inx
        self.ny = iny
        self.framebuf = framebuf.FrameBuffer(self.buffer, inx, iny, framebuf.MONO_HLSB)
        # Provide methods for accessing FrameBuffer graphics primitives. This is a workround
        # because inheritance from a native class is currently unsupported.
        # http://docs.micropython.org/en/latest/pyboard/library/framebuf.html
        self.fill = self.framebuf.fill  # (col)
        self.pixel = self.framebuf.pixel # (x, y[, c])
        self.hline = self.framebuf.hline  # (x, y, w, col)
        self.vline = self.framebuf.vline  # (x, y, h, col)
        self.line = self.framebuf.line  # (x1, y1, x2, y2, col)
        self.rect = self.framebuf.rect  # (x, y, w, h, col)
        self.fill_rect = self.framebuf.fill_rect  # (x, y, w, h, col)
        self.text = self.framebuf.text  # (string, x, y, col=1)
        self.scroll = self.framebuf.scroll  # (dx, dy)
        self.blit = self.framebuf.blit  # (fbuf, x, y[, key])
        
    def write(self,v: []) -> none:
        y=self.ny-1
        for s in v:
            x=self.nx-1
            for c in s:
                if c=='1':
                    self.pixel(x,y,1)
                x -=1
                if (x<0):
                    break                
            y -= 1
            if (y<0):
                break

class NumberDisplay():

    _n = []

    _n.append(["-1111-",
        "11--11",
        "11--11",
        "11--11",
        "11--11",
        "-1111-" ])

    _n.append(["--11--",
        "-111--",
        "--11--",
        "--11--",
        "--11--",
        "-1111-"])

    _n.append(["-1111-",
        "11--11",
        "---11-",
        "--11--",
        "-11---",
        "111111"])

    _n.append(["-1111-",
        "1---11",
        "--111-",
        "----11",
        "11--11",
        "-1111-"])

    _n.append(["---11-",
        "--111-",
        "-1111-",
        "11-11-",
        "111111",
        "---11-"])

    _n.append(["111111",
        "11----",
        "11111-",
        "----11",
        "11--11",
        "-1111-"])

    _n.append(["-1111-",
        "11----",
        "11111-",
        "11--11",
        "11--11",
        "-1111-"])

    _n.append(["111111",
        "----11",
        "---11-",
        "--11--",
        "--11--",
        "--11--"])

    _n.append(["-1111-",
        "11--11",
        "-1111-",
        "11--11",
        "11--11",
        "-1111-"])

    _n.append(["-1111-",
        "11--11",
        "11--11",
        "-11111",
        "---11-",
        "-111--"])

    def __init__(self):
        self.fb2d = [] #(6,6)
        # setup the framebuffer for numbers & :
        for i in range(10):
            self.fb2d.append(MyBuffer2D(6,6))
            self.fb2d[i].write(NumberDisplay._n[i])

    def fb(self,v: str) -> framebuf.FrameBuffer:
        i = int(v)
        assert i <= 9 and i >=0
        return self.fb2d[i].framebuf

class TextDisplay:

    _nd=["-11-",
        "-11-",
        "----",
        "----",
        "-11-",
        "-11-"]

    _no=["-1--1----1--111-1--1----1--1--1-",
        "1-1-1---1-1-1-1-1111-1-1-1-11-1-",
        "111-1---111-11--1--1---1-1-1111-",
        "1-1-1---1-1-1-1-1--1-1-1-1-1-11-",
        "1-1-111-1-1-1-1-1--1----1--1--1-"]

    _nf=["-1--1----1--111-1--1----1--11-11",
        "1-1-1---1-1-1-1-1111-1-1-1-1--1-",
        "111-1---111-11--1--1---1-1-11-11",
        "1-1-1---1-1-1-1-1--1-1-1-1-1--1-",
        "1-1-111-1-1-1-1-1--1----1--1--1-"]

    _nl=["----1----111--111-1--1-11111----",
         "----1-----1--1----1--1---1------",
         "----1-----1--1-11-1111---1------",
         "----1-----1--1--1-1--1---1------",
         "----1111-111--111-1--1---1------"]

    def __init__(self):
        self.fb2d = [] #(6,6)
        # setup the framebuffer 
        self.fb2d.append(MyBuffer2D(4,6))
        self.fb2d[0].write(TextDisplay._nd)
        self.fb2d.append(MyBuffer2D(32,5))
        self.fb2d[1].write(TextDisplay._no)
        self.fb2d.append(MyBuffer2D(32,5))
        self.fb2d[2].write(TextDisplay._nf)
        self.fb2d.append(MyBuffer2D(32,5))
        self.fb2d[3].write(TextDisplay._nl)

    def fb(self,v: str) -> framebuf.FrameBuffer:
        if v == ":":
            return self.fb2d[0].framebuf
        if v == "alarm:on":
            return self.fb2d[1].framebuf
        if v == "alarm:off":
            return self.fb2d[2].framebuf
        if v == "light":
            return self.fb2d[3].framebuf
        
        assert False



