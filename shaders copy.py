vertex_shader = """
#version 330
layout(location = 0) in vec3 a_position;
layout(location = 1) in vec2 a_texture;
layout(location = 2) in vec3 a_normal;

out vec2 v_texture;
out vec3 v_normal;
out vec3 v_frag_pos;

uniform mat4 model;
uniform mat4 projection;
uniform mat4 view;

void main()
{
    gl_Position = projection * view * model * vec4(a_position, 1.0);
    v_texture = a_texture;
    
    // Transform the normal to view space
    mat3 normalMatrix = transpose(inverse(mat3(model)));
    v_normal = normalize(normalMatrix * a_normal);
    
    // Calculate fragment position in view space
    v_frag_pos = vec3(view * model * vec4(a_position, 1.0));
}
"""

fragment_shader = """
#version 330

in vec2 v_texture;
in vec3 v_normal;
in vec3 v_frag_pos;

out vec4 out_color;

uniform sampler2D s_texture;
uniform ivec3 icolor;
uniform int switcher;

struct Light {
    vec3 position;
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
};

uniform Light light;
uniform vec3 viewPos;
uniform float shininess;

void main()
{
    vec3 ambient = light.ambient * texture(s_texture, v_texture).rgb;
    
    // Diffuse
    vec3 norm = normalize(v_normal);
    vec3 lightDir = normalize(light.position - v_frag_pos);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = light.diffuse * diff * texture(s_texture, v_texture).rgb;
    
    // Specular
    vec3 viewDir = normalize(viewPos - v_frag_pos);
    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), shininess);
    vec3 specular = light.specular * spec;
    
    vec3 result = ambient + diffuse + specular;
    out_color = vec4(result, 1.0);
}
"""

# You would need to set the light properties and other uniforms in your OpenGL code.
