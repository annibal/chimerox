#!/usr/bin/env python3
"""
Chimerox - Abstract Video Generator
Usage: python chimerox.py [options] filename
"""

import argparse
import cv2
import numpy as np
import math
import random
import colorsys
from pathlib import Path

class Chimerox:
    def __init__(self, iota, omicron, phase, threshold, resonance, entropy, width, height, duration, fps=24):
        self.iota = iota
        self.omicron = omicron
        self.phase = phase
        self.threshold = threshold
        self.resonance = resonance
        self.entropy = entropy
        self.width = width
        self.height = height
        self.duration = duration
        self.fps = fps
        self.total_frames = duration * fps
        
        # Seed-based initialization
        random.seed(iota)
        np.random.seed(iota % 2**32)
        
        # Generate particles based on threshold (reduced greatly)
        self.num_particles = int(threshold * 0.15 * (0.3 + entropy * 0.7))
        self.particles = self._init_particles()
        
        # Color system based on seeds
        self.base_hue = (iota % 360) / 360.0
        self.hue_shift = (omicron % 100) / 100.0
        
        # Bokeh system (more integrated)
        self.bokeh_particles = self._init_bokeh()
        self.bokeh_movement_speed = 0.8 + entropy * 0.5
        
        # Wave system (flowing ribbons)
        self.wave_count = int(8 + (threshold / 100) * entropy)
        self.wave_curves = 1 + int((omicron % 5) * entropy)
        self.wave_depth = 60 + (threshold / 15) * (1 + abs(phase))
        self.wave_speed = 0.02 + resonance * 0.008
        self.wave_opacity = int(80 + entropy * 120)
        
        # Vortex system (more energy streams)
        self.vortex_centers = self._init_vortex_centers()
        self.vortex_intensity = entropy * resonance * 1.5
        self.vortex_rotation_speed = 0.03 + abs(phase) * 0.05
        
        # Reality Distortion Field (5th element)
        self.distortion_strength = entropy * resonance * 0.3
        self.distortion_type = omicron % 4  # 0=spiral, 1=circular, 2=radial, 3=wave
        self.distortion_speed = 0.02 + abs(phase) * 0.03
        self.distortion_centers = self._init_distortion_centers()
        
    def _init_particles(self):
        particles = []
        for i in range(self.num_particles):
            # Use both seeds for particle properties
            seed_offset = (self.iota + i * self.omicron) % 10000
            random.seed(seed_offset)
            
            particle = {
                'x': random.uniform(0, self.width),
                'y': random.uniform(0, self.height),
                'vx': random.uniform(-4, 4) * self.entropy,
                'vy': random.uniform(-4, 4) * self.entropy,
                'size': random.uniform(2, 12),
                'age': 0,
                'life': random.uniform(80, 300),
                'orbit_radius': random.uniform(20, 200),
                'orbit_speed': random.uniform(0.02, 0.08) * self.resonance,
                'color_offset': random.uniform(0, 1)
            }
            particles.append(particle)
        return particles
    
    def _init_bokeh(self):
        """Initialize bokeh background particles"""
        bokeh_count = int(25 + self.threshold * 0.08)
        bokeh_particles = []
        
        for i in range(bokeh_count):
            # Palette range based on omicron (wider range)
            palette_range = (self.omicron % 300) / 300.0  # 0-300 degrees
            hue_variation = (random.random() - 0.5) * palette_range
            hue = (self.base_hue + hue_variation) % 1.0
            
            bokeh = {
                'x': random.uniform(-100, self.width + 100),
                'y': random.uniform(-100, self.height + 100),
                'size': random.uniform(40, 180),
                'hue': hue,
                'flicker_offset': random.uniform(0, math.pi * 2),
                'movement_angle': random.uniform(0, math.pi * 2),
                'depth': random.uniform(0.4, 1.2)  # for layering
            }
            bokeh_particles.append(bokeh)
        
        return bokeh_particles
    
    def _init_vortex_centers(self):
        """Initialize vortex centers for the 4th effect"""
        vortex_count = int(2 + (self.entropy * 3))
        centers = []
        
        for i in range(vortex_count):
            center = {
                'x': random.uniform(0.2 * self.width, 0.8 * self.width),
                'y': random.uniform(0.2 * self.height, 0.8 * self.height),
                'orbit_radius': random.uniform(50, 150),
                'orbit_speed': random.uniform(0.005, 0.02) * self.resonance,
                'strength': random.uniform(0.5, 1.5) * self.entropy
            }
            centers.append(center)
        
        return centers
    
    def _init_distortion_centers(self):
        """Initialize distortion centers for reality warping"""
        if self.distortion_strength < 0.1:
            return []
        
        center_count = int(1 + (self.entropy * 2))
        centers = []
        
        for i in range(center_count):
            center = {
                'x': random.uniform(0.3 * self.width, 0.7 * self.width),
                'y': random.uniform(0.3 * self.height, 0.7 * self.height),
                'strength': random.uniform(0.5, 1.5) * self.distortion_strength,
                'radius': random.uniform(100, min(self.width, self.height) * 0.4),
                'rotation_speed': random.uniform(0.005, 0.02) * self.distortion_speed,
                'phase_offset': random.uniform(0, math.pi * 2)
            }
            centers.append(center)
        
        return centers
    
    def _get_color(self, t, particle):
        # Complex color calculation using all parameters
        base_t = (t + self.phase) * self.resonance
        hue_mod = (self.base_hue + 
                  particle['color_offset'] * self.hue_shift + 
                  math.sin(base_t * 0.01) * 0.2) % 1.0
        
        saturation = 0.7 + 0.3 * math.sin(base_t * 0.02 + particle['age'] * 0.1)
        value = 0.8 + 0.2 * math.cos(base_t * 0.03)
        
        rgb = colorsys.hsv_to_rgb(hue_mod, saturation, value)
        return tuple(int(c * 255) for c in rgb)
    
    def _update_particle(self, particle, frame):
        t = frame + self.phase * 1000
        
        # Movement based on multiple forces
        wave_force = math.sin(t * 0.01 + particle['x'] * 0.01) * self.resonance
        chaos_force = (random.random() - 0.5) * self.entropy * 2
        
        # Orbital motion influenced by omicron seed
        orbit_t = t * particle['orbit_speed'] + (self.omicron % 1000) * 0.01
        orbit_x = math.cos(orbit_t) * particle['orbit_radius']
        orbit_y = math.sin(orbit_t) * particle['orbit_radius']
        
        # Update velocity
        particle['vx'] += wave_force * 0.1 + chaos_force
        particle['vy'] += math.cos(t * 0.008) * self.resonance * 0.1 + chaos_force
        
        # Apply orbital influence
        center_x = self.width / 2 + orbit_x
        center_y = self.height / 2 + orbit_y
        
        dx = center_x - particle['x']
        dy = center_y - particle['y']
        dist = math.sqrt(dx*dx + dy*dy)
        
        if dist > 0:
            force = min(1.0, self.threshold / 1000.0)
            particle['vx'] += (dx / dist) * force * 0.02
            particle['vy'] += (dy / dist) * force * 0.02
        
        # Update position
        particle['x'] += particle['vx']
        particle['y'] += particle['vy']
        
        # Boundary wrapping with phase influence
        if particle['x'] < 0 or particle['x'] > self.width:
            particle['x'] = (particle['x'] + self.phase * 100) % self.width
        if particle['y'] < 0 or particle['y'] > self.height:
            particle['y'] = (particle['y'] + self.phase * 100) % self.height
        
        # Age particle
        particle['age'] += 1
        
        # Respawn if dead
        if particle['age'] > particle['life']:
            particle['age'] = 0
            particle['x'] = random.uniform(0, self.width)
            particle['y'] = random.uniform(0, self.height)
            particle['life'] = random.uniform(50, 200)
    
    def _draw_frame(self, frame):
        # Create frame with fading trail effect
        canvas = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # Background gradient influenced by phase
        bg_intensity = int(20 + 10 * math.sin(frame * 0.01 + self.phase))
        canvas[:] = (bg_intensity, bg_intensity//2, bg_intensity//3)
        
        # 1. Draw bokeh background
        self._draw_bokeh(canvas, frame)
        
        # 2. Draw wave effects
        self._draw_waves(canvas, frame)
        
        # 3. Draw vortex distortion field
        self._draw_vortex_field(canvas, frame)
        
        # 4. Draw main particles on top
        for particle in self.particles:
            self._update_particle(particle, frame)
            
            color = self._get_color(frame, particle)
            
            # Draw particle with varying effects
            x, y = int(particle['x']), int(particle['y'])
            size = int(particle['size'] * (1 + math.sin(frame * 0.02) * 0.3))
            
            if 0 <= x < self.width and 0 <= y < self.height:
                # Main particle
                cv2.circle(canvas, (x, y), size, color, -1)
                
                # Glow effect based on entropy
                if self.entropy > 0.5:
                    glow_size = size + 3
                    glow_color = tuple(int(c * 0.3) for c in color)
                    cv2.circle(canvas, (x, y), glow_size, glow_color, 1)
                
                # Trail effect (longer, more fluid)
                trail_length = int(12 + self.resonance * 8)
                for i in range(1, trail_length):
                    trail_x = int(x - particle['vx'] * i * 0.8)
                    trail_y = int(y - particle['vy'] * i * 0.8)
                    if 0 <= trail_x < self.width and 0 <= trail_y < self.height:
                        alpha = 1.0 - (i / trail_length)
                        trail_color = tuple(int(c * alpha * 0.8) for c in color)
                        trail_size = max(1, int(size * alpha))
                        cv2.circle(canvas, (trail_x, trail_y), trail_size, trail_color, -1)
        
        # 5. Apply REALITY DISTORTION FIELD (The 5th Element)
        canvas = self._apply_reality_distortion(canvas, frame)
        
        return canvas
    
    def _draw_bokeh(self, canvas, frame):
        """Draw bokeh background particles"""
        # Brightness based on phase (-1 dark, 1 bright) - brighter overall
        brightness = 0.5 + (self.phase + 1) * 0.4  # maps -1,1 to 0.5,1.3
        
        for bokeh in self.bokeh_particles:
            # More dynamic movement
            movement_speed = self.bokeh_movement_speed * 0.3
            bokeh['x'] += math.cos(bokeh['movement_angle']) * movement_speed
            bokeh['y'] += math.sin(bokeh['movement_angle']) * movement_speed
            
            # Wrap around when going off canvas
            if bokeh['x'] < -150: bokeh['x'] = self.width + 100
            if bokeh['x'] > self.width + 150: bokeh['x'] = -100
            if bokeh['y'] < -150: bokeh['y'] = self.height + 100
            if bokeh['y'] > self.height + 150: bokeh['y'] = -100
            
            # More dynamic flicker
            flicker_t = frame * 0.008 + bokeh['flicker_offset']
            flicker = 0.7 + 0.3 * math.sin(flicker_t) * math.cos(flicker_t * 1.7)
            
            # Brighter, more saturated colors
            saturation = 0.7 + 0.3 * math.sin(frame * 0.002 + bokeh['hue'] * 10)
            value = brightness * flicker * bokeh['depth']
            
            rgb = colorsys.hsv_to_rgb(bokeh['hue'], saturation, value)
            color = tuple(int(c * 255) for c in rgb)
            
            # Draw larger, more prominent bokeh
            x, y = int(bokeh['x']), int(bokeh['y'])
            size = int(bokeh['size'] * (0.8 + 0.2 * flicker))
            
            if -size <= x <= self.width + size and -size <= y <= self.height + size:
                # Create stronger gradient effect
                for radius in range(size, 0, -max(1, size//6)):
                    alpha = (1.0 - radius/size) * 0.6
                    fade_color = tuple(int(c * alpha) for c in color)
                    cv2.circle(canvas, (x, y), radius, fade_color, -1)
    
    def _draw_waves(self, canvas, frame):
        """Draw wave effects between bokeh and particles"""
        t = frame * self.wave_speed
        
        for wave_idx in range(self.wave_count):
            wave_offset = wave_idx * (math.pi * 2 / self.wave_count)
            
            # More dynamic wave parameters
            frequency = 0.008 + (self.resonance * 0.003)
            amplitude = self.wave_depth * (0.8 + 0.4 * math.sin(t + wave_offset))
            
            # Create flowing wave path with diagonal flow
            points = []
            for x in range(0, self.width, max(1, int(self.width // 300))):
                # More complex wave with diagonal bias
                y_base = self.height // 3 + (wave_idx * self.height // (self.wave_count + 1))
                
                # Primary flowing wave
                wave1 = amplitude * math.sin(x * frequency + t * 2 + wave_offset)
                
                # Diagonal flow component
                diagonal_flow = (x / self.width) * 150 * math.sin(t * 0.5 + wave_offset)
                
                # Multiple harmonics for complexity
                wave2 = (amplitude * 0.4) * math.sin(x * frequency * 1.8 + t * 1.3 + wave_offset)
                wave3 = (amplitude * 0.2) * math.cos(x * frequency * 0.6 + t * 0.7 + wave_offset)
                
                y = int(y_base + wave1 + wave2 + wave3 + diagonal_flow)
                points.append((x, y))
            
            # Draw wave with much more vibrant colors
            hue = (self.base_hue + wave_idx * 0.15 + t * 0.02) % 1.0
            
            # Higher saturation and brightness
            saturation = 0.8 + self.resonance * 0.2
            value = 0.8 + 0.2 * math.sin(t * 3 + wave_offset)
            
            rgb = colorsys.hsv_to_rgb(hue, saturation, value)
            wave_color = tuple(int(c * 255) for c in rgb)
            
            # Draw thicker waves with stronger glow
            thickness = max(2, int(6 + self.entropy * 8))
            
            for i in range(len(points) - 1):
                x1, y1 = points[i]
                x2, y2 = points[i + 1]
                
                if 0 <= y1 < self.height and 0 <= y2 < self.height:
                    # Stronger glow first
                    glow_color = tuple(int(c * 0.4) for c in wave_color)
                    cv2.line(canvas, (x1, y1), (x2, y2), glow_color, thickness + 8)
                    
                    # Main wave line
                    cv2.line(canvas, (x1, y1), (x2, y2), wave_color, thickness)
    
    def _draw_vortex_field(self, canvas, frame):
        """Draw 4th effect: vortex distortion field"""
        if self.vortex_intensity < 0.3:
            return
        
        t = frame * 0.01
        
        # Create energy field visualization
        for vortex in self.vortex_centers:
            # Update vortex center position
            orbit_t = t * vortex['orbit_speed']
            center_x = vortex['x'] + math.cos(orbit_t) * 30
            center_y = vortex['y'] + math.sin(orbit_t) * 30
            
            # Draw energy spirals around vortex
            spiral_points = int(20 + self.threshold * 0.1)
            
            for spiral_idx in range(spiral_points):
                angle_step = (spiral_idx / spiral_points) * math.pi * 4
                radius = spiral_idx * 2 + 10
                
                # Spiral rotation
                rotation = t * self.vortex_rotation_speed + angle_step
                
                x = center_x + math.cos(rotation) * radius
                y = center_y + math.sin(rotation) * radius
                
                if 0 <= x < self.width and 0 <= y < self.height:
                    # Energy particle color
                    energy_hue = (self.base_hue + rotation * 0.1) % 1.0
                    energy_saturation = 0.8 + 0.2 * math.sin(t * 3 + spiral_idx)
                    energy_value = vortex['strength'] * (1 - spiral_idx / spiral_points) * 0.8
                    
                    rgb = colorsys.hsv_to_rgb(energy_hue, energy_saturation, energy_value)
                    energy_color = tuple(int(c * 255) for c in rgb)
                    
                    # Draw energy particle
                    particle_size = max(1, int(3 * vortex['strength'] * (1 - spiral_idx / spiral_points)))
                    cv2.circle(canvas, (int(x), int(y)), particle_size, energy_color, -1)
                    
                    # Add connecting lines for energy flow
                    if spiral_idx > 0 and spiral_idx % 3 == 0:
                        prev_angle = ((spiral_idx - 3) / spiral_points) * math.pi * 4
                        prev_radius = (spiral_idx - 3) * 2 + 10
                        prev_rotation = t * self.vortex_rotation_speed + prev_angle
                        
                        prev_x = center_x + math.cos(prev_rotation) * prev_radius
                        prev_y = center_y + math.sin(prev_rotation) * prev_radius
                        
                        if 0 <= prev_x < self.width and 0 <= prev_y < self.height:
                            line_color = tuple(int(c * 0.4) for c in energy_color)
                            cv2.line(canvas, (int(prev_x), int(prev_y)), (int(x), int(y)), line_color, 1)
    
    def _apply_reality_distortion(self, canvas, frame):
        """Apply reality distortion field - The 5th Element"""
        if self.distortion_strength < 0.05:
            return canvas
        
        t = frame * self.distortion_speed
        height, width = canvas.shape[:2]
        
        # Skip pixels for performance - adaptive step size
        step = max(1, int(4 - self.distortion_strength * 8))  # More strength = smaller step
        
        # Create displacement maps with reduced resolution
        map_x = np.zeros((height, width), dtype=np.float32)
        map_y = np.zeros((height, width), dtype=np.float32)
        
        # Initialize with identity mapping
        for y in range(height):
            for x in range(width):
                map_x[y, x] = x
                map_y[y, x] = y
        
        # Apply distortions from each center (with pixel skipping)
        for center in self.distortion_centers:
            center_x = center['x'] + 20 * math.cos(t * center['rotation_speed'] + center['phase_offset'])
            center_y = center['y'] + 20 * math.sin(t * center['rotation_speed'] + center['phase_offset'])
            
            for y in range(0, height, step):
                for x in range(0, width, step):
                    # Distance from distortion center
                    dx = x - center_x
                    dy = y - center_y
                    distance = math.sqrt(dx*dx + dy*dy)
                    
                    if distance < center['radius'] and distance > 1:
                        # Calculate distortion based on type
                        influence = (1.0 - distance / center['radius']) * center['strength']
                        
                        # Calculate displacement
                        offset_x, offset_y = 0, 0
                        
                        if self.distortion_type == 0:  # Spiral
                            angle = math.atan2(dy, dx) + influence * 2 + t
                            new_dist = distance * (1 + influence * 0.1 * math.sin(distance * 0.05 + t))
                            offset_x = math.cos(angle) * new_dist - dx
                            offset_y = math.sin(angle) * new_dist - dy
                            
                        elif self.distortion_type == 1:  # Circular ripple
                            ripple = math.sin(distance * 0.1 - t * 3) * influence * 10
                            if distance > 0:
                                offset_x = (dx / distance) * ripple
                                offset_y = (dy / distance) * ripple
                                
                        elif self.distortion_type == 2:  # Radial zoom
                            zoom_factor = 1 + influence * 0.3 * math.sin(t * 2)
                            offset_x = dx * (zoom_factor - 1)
                            offset_y = dy * (zoom_factor - 1)
                            
                        elif self.distortion_type == 3:  # Wave distortion
                            offset_x = influence * 15 * math.sin(y * 0.02 + t * 2)
                            offset_y = influence * 15 * math.cos(x * 0.02 + t * 1.7)
                        
                        # Apply offset to current pixel and fill neighboring pixels
                        for fy in range(y, min(y + step, height)):
                            for fx in range(x, min(x + step, width)):
                                map_x[fy, fx] += offset_x
                                map_y[fy, fx] += offset_y
        
        # Apply bounds checking
        map_x = np.clip(map_x, 0, width - 1)
        map_y = np.clip(map_y, 0, height - 1)
        
        # Apply the distortion using remap
        distorted = cv2.remap(canvas, map_x, map_y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        
        # Blend with original for subtle effect
        blend_factor = min(1.0, self.distortion_strength * 2)
        result = cv2.addWeighted(canvas, 1 - blend_factor, distorted, blend_factor, 0)
        
        return result
    
    def generate(self, output_path, metadata=None, codec=None):
        # Auto-detect codec from extension or use provided
        if codec:
            fourcc_code = codec
        else:
            ext = output_path.suffix.lower()
            codec_map = {
                '.mp4': 'mp4v',
                '.avi': 'XVID', 
                '.wmv': 'WMV2',
                '.mov': 'MJPG'
            }
            fourcc_code = codec_map.get(ext, 'mp4v')
            
            # If no extension or unknown, force .mp4
            if ext not in codec_map:
                output_path = output_path.with_suffix('.mp4')
        
        fourcc = cv2.VideoWriter_fourcc(*fourcc_code)
        out = cv2.VideoWriter(str(output_path), fourcc, self.fps, (self.width, self.height))
        
        print(f"Generating {self.total_frames} frames...")
        
        for frame in range(self.total_frames):
            if frame % 30 == 0:  # Progress every second
                print(f"Frame {frame}/{self.total_frames} ({frame/self.total_frames*100:.1f}%)")
            
            canvas = self._draw_frame(frame)
            out.write(canvas)
        
        out.release()
        print(f"Video saved to {output_path}")
        
        # Add metadata if ffmpeg available
        if metadata:
            self._add_metadata(output_path, metadata)
    
    def _add_metadata(self, video_path, metadata):
        try:
            import subprocess
            temp_path = video_path.with_suffix('.temp.mp4')
            
            cmd = ['ffmpeg', '-i', str(video_path), '-c', 'copy']
            for key, value in metadata.items():
                cmd.extend(['-metadata', f'{key}={value}'])
            cmd.append(str(temp_path))
            
            subprocess.run(cmd, check=True, capture_output=True)
            temp_path.replace(video_path)
            print("Metadata added successfully")
        except:
            print("Warning: Could not add metadata (ffmpeg not available)")

def parse_dimensions(dim_str):
    # Find separator (any non-numeric character)
    separator_idx = -1
    for i, char in enumerate(dim_str):
        if not char.isdigit():
            separator_idx = i
            break
    
    if separator_idx == -1:
        raise ValueError("Invalid dimensions format. Use WIDTH{separator}HEIGHT")
    
    width = int(dim_str[:separator_idx])
    height = int(dim_str[separator_idx+1:])
    
    if width <= 0 or height <= 0:
        raise ValueError("Width and height must be positive integers")
    
    return width, height

def validate_codec(codec, filename):
    """Validate codec and fix filename extension if incompatible"""
    valid_codecs = ['mp4v', 'XVID', 'MJPG', 'X264', 'DIVX', 'WMV1', 'WMV2', 'FMP4', 'H264']
    
    if codec not in valid_codecs:
        raise ValueError(f"Invalid codec '{codec}'. Valid codecs: {', '.join(valid_codecs)}")
    
    # Codec to preferred extension mapping
    codec_to_ext = {
        'mp4v': '.mp4', 'X264': '.mp4', 'H264': '.mp4', 'FMP4': '.mp4',
        'XVID': '.avi', 'DIVX': '.avi', 'MJPG': '.avi',
        'WMV1': '.wmv', 'WMV2': '.wmv'
    }
    
    # Compatible extensions for each codec
    compatible_codecs = {
        '.mp4': ['mp4v', 'X264', 'H264', 'FMP4'],
        '.avi': ['XVID', 'DIVX', 'MJPG'],
        '.wmv': ['WMV1', 'WMV2'],
        '.mov': ['mp4v', 'MJPG']
    }
    
    filepath = Path(filename)
    current_ext = filepath.suffix.lower()
    
    # Check if current extension is compatible with codec
    is_compatible = False
    for ext, codecs in compatible_codecs.items():
        if current_ext == ext and codec in codecs:
            is_compatible = True
            break
    
    # If not compatible, change extension
    if not is_compatible:
        new_ext = codec_to_ext[codec]
        new_filepath = filepath.with_suffix(new_ext)
        print(f"Warning: Codec '{codec}' not compatible with '{current_ext}' extension")
        print(f"Changed filename from '{filename}' to '{new_filepath}'")
        return codec, str(new_filepath)
    
    return codec, filename

def parse_metadata(meta_list):
    metadata = {}
    for meta in meta_list:
        if ':' in meta:
            key, value = meta.split(':', 1)
            metadata[key] = value
    return metadata

def main():
    parser = argparse.ArgumentParser(
        description='Chimerox - Abstract Video Generator',
        epilog='''
Examples:
  %(prog)s video.mp4
  %(prog)s -i 12345 -p 0.5 output.avi
  %(prog)s --FHD --portrait video.mp4               # 1080x1920 portrait
  %(prog)s --QHD -c X264 -m Title:MyVideo video.mp4
  %(prog)s -t 1000 -e 0.8 -n 3.0 chaos.mp4

Parameter ranges:
  iota (-i):      [-16581375, 16581375] (random if not set)
  omicron (-o):   [-604800, 604800] (random if not set)  
  phase (-p):     [-1.0, 1.0] (random if not set)
  threshold (-t): positive integer (default: 500)
  resonance (-n): float (default: 2.0)
  entropy (-e):   float (default: 0.5)
  fps (-f):       [1, 200] (default: 24)
  
Resolution presets:
  --QHD: 960x540    --XGA: 1024x768   --HD: 1366x768     --HDV: 1440x1080
  --FHD: 1920x1080  --UXGA: 1600x1200 --WQHD: 2560x1440  --QVGA: 320x240
  -l, --landscape: force 960x540     --portrait: swap width/height
  
Supported codecs:
  mp4v, XVID, MJPG, X264, DIVX, WMV1, WMV2, FMP4, H264
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('filename', nargs='?', help='Output video filename')
    parser.add_argument('-i', '--iota', type=int, default=None, metavar='N', 
                       help='Primary seed [-16581375 to 16581375] (random if omitted)')
    parser.add_argument('-o', '--omicron', type=int, default=None, metavar='N',
                       help='Secondary seed [-604800 to 604800] (random if omitted)')
    parser.add_argument('-p', '--phase', type=float, default=None, metavar='F',
                       help='Temporal offset [-1.0 to 1.0] (random if omitted)')
    parser.add_argument('-t', '--threshold', type=int, default=500, metavar='N',
                       help='Density cap (default: 500)')
    parser.add_argument('-n', '--resonance', type=float, default=2.0, metavar='F',
                       help='Frequency of mutations (default: 2.0)')
    parser.add_argument('-e', '--entropy', type=float, default=0.5, metavar='F',
                       help='Chaos vs order [0-1] (default: 0.5)')
    parser.add_argument('-s', '--dimensions', '--size', type=str, default='640x480', metavar='WxH',
                       help='Custom dimensions WIDTH{sep}HEIGHT (default: 640x480)')
    parser.add_argument('-d', '--length', '--duration', type=int, default=10, metavar='N',
                       help='Duration in seconds (default: 10)')
    parser.add_argument('-f', '--fps', type=int, default=24, metavar='N',
                       help='Frames per second [1-200] (default: 24)')
    parser.add_argument('-c', '--codec', type=str, metavar='CODEC',
                       help='Force codec, overrides auto-detection')
    parser.add_argument('-m', '--meta', action='append', default=[], metavar='KEY:VALUE',
                       help='Add metadata (can be used multiple times)')
    
    # Resolution presets
    parser.add_argument('-l', '--landscape', action='store_true', help='Set to 960x540 landscape')
    parser.add_argument('--portrait', action='store_true', help='Swap width/height for portrait mode')
    parser.add_argument('-r', '--resolution', type=str, choices=['QHD', 'XGA', 'HD', 'HDV', 'FHD', 'UXGA', 'WQHD', 'QVGA'],
                       metavar='PRESET', help='Resolution preset')
    
    # Resolution preset flags
    parser.add_argument('--QHD', action='store_const', const='QHD', dest='preset_resolution', help='960x540')
    parser.add_argument('--XGA', action='store_const', const='XGA', dest='preset_resolution', help='1024x768')
    parser.add_argument('--HD', action='store_const', const='HD', dest='preset_resolution', help='1366x768')
    parser.add_argument('--HDV', action='store_const', const='HDV', dest='preset_resolution', help='1440x1080')
    parser.add_argument('--FHD', action='store_const', const='FHD', dest='preset_resolution', help='1920x1080')
    parser.add_argument('--UXGA', action='store_const', const='UXGA', dest='preset_resolution', help='1600x1200')
    parser.add_argument('--WQHD', action='store_const', const='WQHD', dest='preset_resolution', help='2560x1440')
    parser.add_argument('--QVGA', action='store_const', const='QVGA', dest='preset_resolution', help='320x240')
    
    args = parser.parse_args()
    
    # Check filename
    if not args.filename:
        print("Chimerox: filename argument was not provided")
        parser.print_help()
        return 1
    
    # Handle resolution conflicts and determine final dimensions
    resolution_sources = []
    if args.landscape:
        resolution_sources.append('landscape')
    if args.resolution:
        resolution_sources.append(f'--resolution={args.resolution}')
    if args.preset_resolution:
        resolution_sources.append(f'--{args.preset_resolution}')
    if args.dimensions != '640x480':  # Non-default dimensions
        resolution_sources.append('--dimensions')
    
    # Check for ambiguous resolutions (portrait is exception)
    non_portrait_sources = [s for s in resolution_sources if s != 'portrait']
    if len(non_portrait_sources) > 1:
        print(f"Ambiguous resolutions provided: {', '.join(non_portrait_sources)}")
        return 1
    
    # Determine base resolution
    resolution_presets = {
        'QHD': (960, 540),
        'XGA': (1024, 768), 
        'HD': (1366, 768),
        'HDV': (1440, 1080),
        'FHD': (1920, 1080),
        'UXGA': (1600, 1200),
        'WQHD': (2560, 1440),
        'QVGA': (320, 240)
    }
    
    if args.landscape:
        width, height = 960, 540
    elif args.resolution:
        width, height = resolution_presets[args.resolution]
    elif args.preset_resolution:
        width, height = resolution_presets[args.preset_resolution]
    else:
        width, height = parse_dimensions(args.dimensions)
    
    # Apply portrait mode (swap dimensions)
    if args.portrait:
        width, height = height, width
    
    # Validate and set defaults for random parameters
    if args.iota is None:
        args.iota = random.randint(-16581375, 16581375)
        print(f"Using random iota: {args.iota}")
    else:
        args.iota = max(-16581375, min(16581375, args.iota))
    
    if args.omicron is None:
        args.omicron = random.randint(-604800, 604800)
        print(f"Using random omicron: {args.omicron}")
    else:
        args.omicron = max(-604800, min(604800, args.omicron))
    
    if args.phase is None:
        args.phase = random.uniform(-1, 1)
        print(f"Using random phase: {args.phase:.3f}")
    else:
        args.phase = max(-1, min(1, args.phase))
    
    # Validate other parameters
    if args.length <= 0:
        raise ValueError("Length must be positive")
    
    if not (1 <= args.fps <= 200):
        raise ValueError("FPS must be between 1 and 200")
    
    # Validate codec if provided
    if args.codec:
        args.codec, args.filename = validate_codec(args.codec, args.filename)
    
    metadata = parse_metadata(args.meta)
    
    generator = Chimerox(
        iota=args.iota,
        omicron=args.omicron,
        phase=args.phase,
        threshold=args.threshold,
        resonance=args.resonance,
        entropy=args.entropy,
        width=width,
        height=height,
        duration=args.length,
        fps=args.fps
    )
    
    output_path = Path(args.filename)
    
    # Add Chimerox parameters as metadata
    chimerox_metadata = {
        'iota': str(args.iota),
        'omicron': str(args.omicron), 
        'phase': str(args.phase),
        'threshold': str(args.threshold),
        'resonance': str(args.resonance),
        'entropy': str(args.entropy),
        'generator': 'Chimerox',
        'dimensions': f'{width}x{height}',
        'fps': str(args.fps),
        'duration': str(args.length)
    }
    
    # Merge with user metadata
    metadata.update(chimerox_metadata)
    
    generator.generate(output_path, metadata, args.codec)

if __name__ == '__main__':
    main()