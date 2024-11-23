from OpenGL.GL import *
import pyrr,os
import numpy as np
from TextureLoader import load_texture
from settings import TEXTURE_FOLDER

class GameObject:
    def __init__(self, position, texture_name, rotation=np.zeros(3)):
        self.position = position
        self.rotation = np.radians(rotation)  # Convert degrees to radians
        self.texture_path = os.path.join(TEXTURE_FOLDER, texture_name)
        self.texture_id = glGenTextures(1) 
        self.texture = load_texture(self.texture_path, self.texture_id)

    def render(self, model_loc, cube):
        translation = pyrr.matrix44.create_from_translation(pyrr.Vector3(self.position))
        rotation_x = pyrr.matrix44.create_from_x_rotation(self.rotation[0])
        rotation_y = pyrr.matrix44.create_from_y_rotation(self.rotation[1])
        rotation_z = pyrr.matrix44.create_from_z_rotation(self.rotation[2])
        model = translation @ rotation_x @ rotation_y @ rotation_z
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glDrawElements(GL_TRIANGLES, cube.indices.size, GL_UNSIGNED_INT, None)
