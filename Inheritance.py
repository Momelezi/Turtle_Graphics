# Classes for polygons, inheritance
import math
import turtle

class Polygon:
    unit = 'cm'
    deg = math.pi / 180 
    rad = 180 / math.pi 

    def __init__(self, edge_lengths, angles_rotate):
        self.edge_lengths = edge_lengths
        self.angles_rotate = angles_rotate
        self.num_edges = len(edge_lengths)
        if self.num_edges != len(angles_rotate):
            print("Warning! Initialising a Polygon object from lists of different lengths!")

    def get_number_edges(self): 
        return self.num_edges

    def is_regular(self): 
        for i in range(1, self.num_edges):
            if self.edge_lengths[i] != self.edge_lengths[0] or self.angles_rotate[i] != self.angles_rotate[0]:
                return False
            else:
                return True

    def mean_edge_length(self):
        sum_lengths = 0
        for length in self.edge_lengths:
            sum_lengths = sum_lengths + length
        return sum_lengths/self.num_edges

    def is_larger(self, other):
        return self.mean_edge_length() > other.mean_edge_length()

    def __str__(self):
        return "Polygon with {0} edges, mean edge length: {1}{2}".format(self.num_edges, self.mean_edge_length(), Polygon.unit)

    def draw(self, t, colour, thickness, left):
        if left:
            angle_multiplier = 1
        else:
            angle_multiplier = -1
        t.pencolor(colour)
        t.pensize(int(thickness)) 
        t.pendown()
        for i in range(self.num_edges):
            t.forward(self.edge_lengths[i])
            t.left(angle_multiplier * self.angles_rotate[i])
	    
    def get_vertices_coordinates(self, left):
        if left:
            angle_multiplier = 1
        else:
            angle_multiplier = -1
				
        output_list = [[0,0]] 
        heading = 0
        x = 0
        y = 0

        for i in range(self.num_edges):
            length = self.edge_lengths[i]
            heading_rad = heading * Polygon.deg
            x = x + length * math.cos(heading_rad)
            y = y + length * math.sin(heading_rad)
            output_list.append([x,y])
            heading = heading + self.angles_rotate[i] * angle_multiplier
        return output_list 

    def closed_polygon(self):
        vertices =  self.get_vertices_coordinates(True)
        last_vertex = vertices[-1]
        acceptable_error = 1e-6
        return math.fabs(last_vertex[0]) <= acceptable_error and math.fabs(last_vertex[1]) <= acceptable_error

    def square_dist(self, point1, point2):
        return (point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2

    def get_diameter(self):
        vertices =  self.get_vertices_coordinates(True)
        sq_dia = 0
        n = len(vertices)
        for i in range(n):
            for j in range(i+1, n):
                sq_dist = self.square_dist(vertices[i],vertices[j]) 
                if sq_dist > sq_dia:
                    sq_dia = sq_dist
                    index_vertex1 = i
                    index_vertex2 = j 
        return [index_vertex1, index_vertex2, math.sqrt(sq_dia)]
						
    def draw_circumscribed_circle(self, t, colour, thickness, left):
        vertexlist = self.get_vertices_coordinates(left)
        diameter_info = self.get_diameter()
        point1 = vertexlist[diameter_info[0]]
        point2 = vertexlist[diameter_info[1]]
        radius = diameter_info[2] / 2 
        center = [(point1[0] + point2[0])/2, (point1[1] + point2[1])/2]
        t.pencolor(colour)
        t.pensize(int(thickness))
        t.penup() 
        t.goto(center[0],center[1]-radius)
        t.setheading(0) 
        t.pendown() 
        t.circle(radius)


class RegularPolygon(Polygon):
    def __init__(self, num_edges, edge_len):
        lengths = [] 
        angles = []
        rotate_angle_value = 360 / num_edges
        for i in range(num_edges):
            lengths.append(edge_len)
            angles.append(rotate_angle_value)
            Polygon.__init__(self, lengths, angles)

    def get_area(self):
        n = self.num_edges
        l = self.edge_lengths[0]
        return n*l*l / (4*math.tan(math.pi/n))

    def is_regular(self):
        return True

    def __str__(self):
        return "Regular polygon with {0} edges (edge length: {1}, inner angles: {2})".format(self.num_edges, self.edge_lengths[0], 180 - self.angles_rotate[0])

    def get_diameter(self):
        vertices =  self.get_vertices_coordinates(True)
        useful_index = self.num_edges // 2
        return [ 0, useful_index, math.sqrt(self.square_dist(vertices[0], vertices[useful_index])) ]

    def draw_circumscribed_circle(self, t, colour, thickness, left):
        vertexlist = self.get_vertices_coordinates(left)
        if self.num_edges % 2 == 0:
            inputlist = self.get_diameter()
            point1 = vertexlist[inputlist[0]]
            point2 = vertexlist[inputlist[1]]
            radius = inputlist[2] / 2
            center = [(point1[0] + point2[0])/2, (point1[1] + point2[1])/2]
        else:
            if left:
                multiplier = 1
            else:
                multiplier = -1
            radius = self.edge_lengths[0] / (2 * math.sin(math.pi/self.num_edges))
            apothem = self.edge_lengths[0] / (2 * math.tan(math.pi/self.num_edges))
            center = [ self.edge_lengths[0] / 2, multiplier * apothem ]
        t.pencolor(colour)
        t.pensize(int(thickness))
        t.penup() 
        t.goto(center[0],center[1]-radius)
        t.setheading(0)
        t.pendown()
        t.circle(radius)


class Triangle(Polygon):
    def __str__(self):
        e = self.edge_lengths
        return "Triangle with edges {0}, {1} and {2}".format(e[0], e[1], e[2])

    def get_height(self):
        base = self.edge_lengths[0]
        h = base/2 * math.tan((180 - self.angles_rotate[0]) * Polygon.deg)
        return h

    def get_area(self):
        h = self.get_height()
        base = self.edge_lengths[0]
        return base*h/2



# TOPLEVEL: TESTS


window = turtle.Screen()
myturtle = turtle.Turtle()




mysquare = Polygon([100,100,100,100],[90,90,90,90])
print(mysquare)
mysquare.draw(myturtle,"red",2,left=True)
print(mysquare.get_vertices_coordinates(True))
print(mysquare.closed_polygon())


angle1 = 180/math.pi * math.asin(0.8)
angle2 = 180/math.pi * math.acos(0.8)
triangle_right = Polygon([400,300,500],[90, 180-angle1, 180-angle2])
print(triangle_right.get_vertices_coordinates(True))
print(triangle_right.closed_polygon())
triangle_right.draw(myturtle,"red",2,left = True)

triangle_right.draw_circumscribed_circle(myturtle, "black", 1, True)
mysquare.draw_circumscribed_circle(myturtle, "black", 1, True)
#square2 = RegularPolygon(4,30)
#print(square2)

myturtle.penup()
myturtle.goto(0,0)
myturtle.setheading(0) # kind of resetting the turtle before the next series of drawings

crazypoly = Polygon([120,66,25,21,110,56,233],[25,33,66,54,89,120,80])
crazypoly.draw(myturtle,"blue",2,True)
crazypoly.draw_circumscribed_circle(myturtle, "black", 1, True)

t = turtle.Turtle() # a new one, at (0,0)
penta = RegularPolygon(5,120)
penta.draw(t,"green",2,False)
penta.draw_circumscribed_circle(t, "green", 1, False)


equi1 = RegularPolygon(3,30) # equilateral triangle with edge length 30
equi2 = Triangle([30,30,30],[120,120,120]) # same polygon in fact

print("area1:", equi1.get_area())
print("area2:", equi2.get_area())

window.mainloop()

