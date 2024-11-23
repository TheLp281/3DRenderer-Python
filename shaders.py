vertex_shader = """
#version 330

layout(location = 0) in vec3 a_position;
layout(location = 1) in vec2 a_texture;
layout(location = 2) in vec3 a_normal; // New input for normals

uniform mat4 model;
uniform mat4 projection;
uniform mat4 view;

out vec2 v_texture;
out vec3 v_normal; // Pass normal to fragment shader

void main()
{
    gl_Position = projection * view * model * vec4(a_position, 1.0);
    v_texture = a_texture;
    v_normal = a_normal; // Pass normal to fragment shader
}


"""

fragment_shader = """
#version 330

in vec2 v_texture;
in vec3 v_normal;

out vec4 frag_color;

uniform sampler2D texture_sampler;
vec3 light_direction = normalize(vec3(0.5, 0.5, 1.0)); // Example light direction
vec3 light_color = vec3(1.0, 1.0, 1.0); // White light
vec3 ambient_color = vec3(0.9,0.9,0.9); // Ambient color


void main()
{
    vec3 normal = normalize(v_normal);
    float diffuse = max(dot(normal, -light_direction), 0.0); // Ensure the light faces the correct direction
    vec3 diffuse_color = texture(texture_sampler, v_texture).rgb * light_color * diffuse;
    vec3 ambient = ambient_color * texture(texture_sampler, v_texture).rgb;

    frag_color = vec4(diffuse_color + ambient, 1.0);
}



"""