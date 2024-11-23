from OpenGL.GL import *
import pyrr
def setup_framebuffer(FBO, width, height):
    glBindFramebuffer(GL_FRAMEBUFFER, FBO)

    # Create a depth attachment
    depth_texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, depth_texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT, width, height, 0, GL_DEPTH_COMPONENT, GL_FLOAT, None)
    glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_TEXTURE_2D, depth_texture, 0)

    # Set the draw buffer and read buffer
    glDrawBuffer(GL_NONE)
    glReadBuffer(GL_NONE)

    glBindFramebuffer(GL_FRAMEBUFFER, 0)
    return depth_texture


def draw_to_framebuffer(framebuffer_object, color_location, pick_colors, cube_positions, cube, model_location):

    glBindFramebuffer(GL_FRAMEBUFFER, framebuffer_object)  # Bind framebuffer

    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    num_colors = len(pick_colors)
    for i in range(len(cube_positions)):
        if i < num_colors:
            pick_model = pyrr.matrix44.create_from_translation(cube_positions[i])
            glUniform3iv(color_location, 1, pick_colors[i])
            glUniformMatrix4fv(model_location, 1, GL_FALSE, pick_model)
            glDrawElements(GL_TRIANGLES, len(cube.indices), GL_UNSIGNED_INT, None)
        

    glBindFramebuffer(GL_FRAMEBUFFER, 0)  # Unbind framebuffer

