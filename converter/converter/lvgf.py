from PIL import Image, ImageOps
import os

def gif_to_lvgl(gif_path, dir, output_c_file):
    img_name = "img"

    # Open the GIF file
    gif = Image.open(gif_path)
    frame_count = gif.n_frames
    width, height = gif.size

    # Prepare the C file header
    with open(output_c_file, "w") as c_file:
        c_file.write("/* futaba best girl */\n\n")
        c_file.write("#include <lvgl.h>\n\n")
        c_file.write(f"#ifndef LV_ATTRIBUTE_MEM_ALIGN\n")
        c_file.write(f"#define LV_ATTRIBUTE_MEM_ALIGN\n")
        c_file.write(f"#endif\n\n")

        for frame_index in range(frame_count):
            gif.seek(frame_index)
            frame = ImageOps.invert(gif.convert("1"))

            frame_data = frame.tobytes()
            data_size = len(frame_data) + 8

            frame_name = f"{img_name}_{frame_index}"

            c_file.write(f"#ifndef LV_ATTRIBUTE_IMG_{frame_name.upper()}\n")
            c_file.write(f"#define LV_ATTRIBUTE_IMG_{frame_name.upper()}\n")
            c_file.write(f"#endif\n\n")
            c_file.write(f"const LV_ATTRIBUTE_MEM_ALIGN LV_ATTRIBUTE_LARGE_CONST "
                         f"LV_ATTRIBUTE_IMG_{frame_name.upper()} uint8_t {frame_name}_map[] = {{\n")
            c_file.write(f"#if CONFIG_NICE_VIEW_WIDGET_INVERTED\n")
            c_file.write(f"    0xff, 0xff, 0xff, 0xff, /*Color of index 0*/\n")
            c_file.write(f"    0x00, 0x00, 0x00, 0xff, /*Color of index 1*/\n")
            c_file.write(f"#else\n")
            c_file.write(f"    0x00, 0x00, 0x00, 0xff, /*Color of index 0*/\n")
            c_file.write(f"    0xff, 0xff, 0xff, 0xff, /*Color of index 1*/\n")
            c_file.write(f"#endif\n\n")
        
            # Write the frame data in hex format, 16 values per line
            for i, byte in enumerate(frame_data):
                if i % 16 == 0:
                    c_file.write("    ")
                c_file.write(f"0x{byte:02X}, ")
                if (i + 1) % 16 == 0:
                    c_file.write("\n")
            if len(frame_data) % 16 != 0:
                c_file.write("\n")

            c_file.write("};\n\n")
            
            c_file.write(f"const lv_img_dsc_t {frame_name} = {{\n")
            c_file.write("  .header.cf = LV_IMG_CF_INDEXED_1BIT,\n")
            c_file.write("  .header.always_zero = 0,\n")
            c_file.write("  .header.reserved = 0,\n")
            c_file.write(f"  .header.w = {width},\n")
            c_file.write(f"  .header.h = {height},\n")
            c_file.write(f"  .data_size = {data_size},\n")
            c_file.write(f"  .data = {frame_name}_map,\n")
            c_file.write("};\n\n")

    return frame_count

def create_edits(file, duration):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    frames = gif_to_lvgl(file, __location__, os.path.join(__location__, '../../boards/shields/nice_view_custom/widgets/art.c'))

    with open(os.path.join(__location__, 'template.c'), 'r') as file:
        lines = file.readlines()
 
    # array of edits
    edits = ''
    for i in range(frames):
        edits += (f"LV_IMG_DECLARE(img_{i});\n")

    edits += ("\nconst lv_img_dsc_t *anim_imgs[] = {\n")
    for i in range(frames):
        edits += (f"    &img_{i},\n")
    edits += ("};\n")

    lines[28] = edits + "\n"
    lines[175] = f"lv_animimg_set_src(art, (const void **) anim_imgs, {frames});\n"
    lines[178] = f"lv_animimg_set_duration(art, {duration*frames});\n"
   
    with open(os.path.join(__location__, '../../boards/shields/nice_view_custom/widgets/status.c'), 'w') as file:
        file.writelines(lines)

    print(f"Applied edits successfully.")