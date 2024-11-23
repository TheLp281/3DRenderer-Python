from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
from settings import *
from cube import Cube
from shaders import vertex_shader, fragment_shader



shader = compileProgram(compileShader(vertex_shader, GL_VERTEX_SHADER), compileShader(fragment_shader, GL_FRAGMENT_SHADER))
# VAO and VBO
VAO = glGenVertexArrays(1)
glBindVertexArray(VAO)



# Cube vertices
cube = Cube()
VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, cube.vertices.nbytes, cube.vertices, GL_STATIC_DRAW)

# Cube Element Buffer Object
EBO = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, cube.indices.nbytes, cube.indices, GL_STATIC_DRAW)

# Cube vertices
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, cube.vertices.itemsize * 5, ctypes.c_void_p(0))

# Cube textures
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, cube.vertices.itemsize * 5, ctypes.c_void_p(12))

glUseProgram(shader)
glClearColor(0, 0.1, 0.1, 1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

projection = pyrr.matrix44.create_perspective_projection_matrix(45, W_WIDTH / W_HEIGHT, 0.1, 100)
view = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.0, 0.0, 0.0]))