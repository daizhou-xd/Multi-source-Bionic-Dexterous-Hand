#!/usr/bin/env python3
"""
XML Generator for MuJoCo Simulation
Generates robot.xml for soft robot simulation
"""

def generate_mujoco_xml(
    xml_path: str,
    stl_name: str,
    unit_height: float,
    scale: float,
    num_units: int,
    joint_type: str,
    joint_limit_deg: float,
    robot_length: float,
    site_points: tuple | None,
    cable_mode: int = 2,
) -> None:
    """
    Generate MuJoCo XML file for spiral robot simulation
    
    Args:
        xml_path: Output XML file path
        stl_name: STL mesh filename
        unit_height: Height of each unit segment
        scale: Scaling factor between units
        num_units: Number of robot units
        joint_type: "hinge" for 2-cable or "ball" for 3-cable
        joint_limit_deg: Joint angle limit in degrees
        robot_length: Total robot length
        site_points: Cable attachment points (x1, y1, x2, y2)
        cable_mode: 2 for 2-cable, 3 for 3-cable
    """
    
    xml_content = f'''<?xml version="1.0" encoding="utf-8"?>
<mujoco model="spiral_robot">
    <compiler angle="radian" meshdir="." />
    
    <option timestep="0.002" iterations="50" solver="Newton" tolerance="1e-10" />
    
    <size nconmax="500" njmax="1000" nstack="10000000" />
    
    <visual>
        <rgba haze="0.15 0.25 0.35 1" />
        <quality shadowsize="2048" />
        <map stiffness="700" />
    </visual>
    
    <asset>
        <mesh name="unit_mesh" file="{stl_name}" scale="{scale:.6f} {scale:.6f} {scale:.6f}" />
        <texture name="groundplane" type="2d" builtin="checker" rgb1=".2 .3 .4" rgb2=".1 .2 .3" 
                 width="100" height="100" mark="cross" markrgb=".8 .8 .8" />
        <material name="groundplane" texture="groundplane" texrepeat="5 5" texuniform="true" reflectance=".2" />
        <material name="robot" rgba="0.6 0.7 0.9 1" />
    </asset>
    
    <worldbody>
        <light directional="true" diffuse=".8 .8 .8" specular=".2 .2 .2" pos="0 0 5" dir="0 0 -1" />
        <light directional="true" diffuse=".4 .4 .4" specular=".1 .1 .1" pos="0 0 4" dir="0 -1 -1" />
        <geom name="ground" type="plane" size="10 10 0.1" material="groundplane" />
        
        <!-- Base anchor -->
        <body name="base" pos="0 0 {unit_height:.6f}">
            <geom name="base_geom" type="box" size="0.05 0.05 0.05" rgba="0.8 0.2 0.2 1" />
            <inertial pos="0 0 0" mass="0.1" diaginertia="0.001 0.001 0.001" />
'''
    
    # Generate robot link chain
    current_body = "base"
    for i in range(num_units):
        unit_scale = scale ** i
        xml_content += f'''
            <!-- Unit {i} -->
            <body name="link_{i}" pos="{unit_height * unit_scale:.6f} 0 0">
                <geom name="geom_{i}" type="mesh" mesh="unit_mesh" material="robot" />
                <inertial pos="{unit_height * unit_scale * 0.5:.6f} 0 0" mass="{0.01 * unit_scale:.6f}" 
                          diaginertia="{0.0001 * unit_scale:.6f} {0.0001 * unit_scale:.6f} {0.0001 * unit_scale:.6f}" />
                
                <!-- Joint -->
                <joint name="joint_{i}" type="{joint_type}" axis="0 0 1" 
                       limited="true" range="-{joint_limit_deg * 0.01745:.6f} {joint_limit_deg * 0.01745:.6f}" 
                       damping="0.1" stiffness="0.5" />
                
                <!-- Cable attachment sites -->
'''
        
        if site_points and cable_mode == 2:
            x1, y1, x2, y2 = site_points
            xml_content += f'''                <site name="cable1_unit{i}" pos="{x1 * unit_scale:.6f} {y1 * unit_scale:.6f} 0" size="0.01" />
                <site name="cable2_unit{i}" pos="{x2 * unit_scale:.6f} {y2 * unit_scale:.6f} 0" size="0.01" />
'''
        elif cable_mode == 3:
            radius = robot_length * 0.1
            xml_content += f'''                <site name="cable1_unit{i}" pos="{unit_height * unit_scale * 0.5:.6f} {radius * unit_scale:.6f} 0" size="0.01" />
                <site name="cable2_unit{i}" pos="{unit_height * unit_scale * 0.5:.6f} {-radius * unit_scale * 0.5:.6f} {radius * unit_scale * 0.866:.6f}" size="0.01" />
                <site name="cable3_unit{i}" pos="{unit_height * unit_scale * 0.5:.6f} {-radius * unit_scale * 0.5:.6f} {-radius * unit_scale * 0.866:.6f}" size="0.01" />
'''
        
        current_body = f"link_{i}"
    
    # Close all body tags
    for i in range(num_units + 1):
        xml_content += '            </body>\n'
    
    xml_content += '''        </body>
    </worldbody>
    
    <actuator>
'''
    
    # Add cable actuators
    for i in range(num_units):
        if cable_mode == 2:
            xml_content += f'''        <position name="cable1_act{i}" site="cable1_unit{i}" kp="100" kv="10" />
        <position name="cable2_act{i}" site="cable2_unit{i}" kp="100" kv="10" />
'''
        elif cable_mode == 3:
            xml_content += f'''        <position name="cable1_act{i}" site="cable1_unit{i}" kp="100" kv="10" />
        <position name="cable2_act{i}" site="cable2_unit{i}" kp="100" kv="10" />
        <position name="cable3_act{i}" site="cable3_unit{i}" kp="100" kv="10" />
'''
    
    xml_content += '''    </actuator>
    
</mujoco>
'''
    
    with open(xml_path, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print(f"Generated MuJoCo XML: {xml_path}")
