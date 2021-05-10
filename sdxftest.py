import sdxf

d=sdxf.Drawing()

#set the color of the text layer to green
d.layers.append(sdxf.Layer(name="textlayer",color=3))

#add drawing elements
d.append(sdxf.Text('Hello World!',point=(3,0),layer="textlayer"))
d.append(sdxf.Line(points=[(0,0),(1,1)], layer="drawinglayer"))

linePoints = [(0,0),(1,1),(1,0),(2,1),(2,0),(3,1),(3,0)]
d.append(sdxf.LwPolyLine(points=linePoints,flag=1, layer="drawinglayer"))

d.saveas('hello_world2.dxf')
