
import sys

import trimesh

import numpy as np

from PIL import Image

from OpenGL import GL
from OpenGL.GL import *
from OpenGL.GLU import *

from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtOpenGLWidgets import QOpenGLWidget

def compile_shader(source, shader_type):

    shader = glCreateShader(shader_type)

    glShaderSource(shader, source)
    glCompileShader(shader)

    return shader

def create_shader_program(vertex_src, fragment_src):

    vs = compile_shader(vertex_src, GL_VERTEX_SHADER)
    fs = compile_shader(fragment_src, GL_FRAGMENT_SHADER)
    program = glCreateProgram()

    glAttachShader(program, vs)
    glAttachShader(program, fs)
    glLinkProgram(program)

    glDeleteShader(vs)
    glDeleteShader(fs)

    return program

class ModelViewer(QOpenGLWidget):

    def __init__(self, modelPath, texturePath):
        super().__init__()

        self.modelPath = modelPath
        self.texturePath = texturePath

    def load_model(self):
        # Load model in Trimesh
        scene = trimesh.load(self.modelPath)
        mesh = trimesh.util.concatenate(tuple(scene.geometry.values()))
        # Create vertices
        vertex_data = []
        
        for face in mesh.faces:
            for idx in face:
                pos = mesh.vertices[idx]
                uv = mesh.visual.uv[idx] if mesh.visual.uv is not None else [0.0, 0.0]
                vertex_data.extend([*pos, *uv])

        vertex_data_np = np.array(vertex_data, dtype=np.float32)
        # VAO + VBO
        vao = glGenVertexArrays(1)
        vbo = glGenBuffers(1)

        glBindVertexArray(vao)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, vertex_data_np.nbytes, vertex_data_np, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(3 * 4))

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
        # Load texture
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)

        image = Image.open(self.texturePath)
        image_data = image.tobytes()
        width, height = image.size

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
        glGenerateMipmap(GL_TEXTURE_2D)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glBindTexture(GL_TEXTURE_2D, 0)
        # Shaders
        vertex_src = """
        #version 330 core
        layout(location = 0) in vec3 aPos;
        layout(location = 1) in vec2 aUV;
        out vec2 TexCoord;
        void main() {
            gl_Position = vec4(aPos, 1.0);
            TexCoord = aUV;
        }
        """

        fragment_src = """
        #version 330 core
        in vec2 TexCoord;
        out vec4 FragColor;
        uniform sampler2D texture1;
        void main() {
            FragColor = texture(texture1, TexCoord);
        }
        """

        shader = create_shader_program(vertex_src, fragment_src)

        return {
            "vao": vao,
            "vbo": vbo,
            "shader": shader,
            "texture": texture,
            "vertex_count": len(vertex_data_np) // 5
        }

    def initializeGL(self):
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glEnable(GL_DEPTH_TEST)

        self.model = self.load_model()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(self.model["shader"])
        glBindVertexArray(self.model["vao"])
        glBindTexture(GL_TEXTURE_2D, self.model["texture"])
        glDrawArrays(GL_TRIANGLES, 0, self.model["vertex_count"])
        glBindVertexArray(0)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    model = 'D:/Desktop/Scripts/NexusExplorer/tools/Nexusvault/output/export/Art/Creature/EldanProtectorBot/EldanProtectorBot_Circuitry/EldanProtectorBot_Circuitry.gltf'
    texture = 'D:/Desktop/Scripts/NexusExplorer/tools/Nexusvault/output/export/Art/Creature/EldanProtectorBot/Textures/EldanProtectorBot_Circuitry_002_Color/EldanProtectorBot_Circuitry_002_Color.png'

    viewer = ModelViewer(model, texture)
    viewer.setWindowTitle("Model Viewer")
    viewer.resize(800, 600)
    viewer.show()
    sys.exit(app.exec())
