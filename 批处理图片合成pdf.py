import os
import img2pdf
from pathlib import Path
import re

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(r'(\d+)', str(s))]

def convert_images_to_pdf():
    # 设置输入和输出目录路径
    input_dir = Path(r"D:\藤本树短篇集 《17－21》 《22－26》 第一话：院子裡有两只鸡")  # 请修改为您的图片文件夹路径
    output_dir = Path(r"D:\pdf_output")  # 请修改为您想要的PDF输出文件夹路径
    pdf_prefix = "藤本树短篇集 《17－21》 《22－26》 "  # 设置PDF文件前缀，可以修改为您想要的前缀
    
    # 创建输出目录（如果不存在）
    output_dir.mkdir(exist_ok=True)
    
    # 支持的图片格式
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp']
    
    # 计数器
    total_folders = 0
    converted_folders = 0
    
    # 检查输入目录是否存在
    if not input_dir.exists():
        print(f"错误：输入路径 '{input_dir}' 不存在！")
        return
    
    # 遍历输入目录下的所有子文件夹
    for folder in input_dir.iterdir():
        if folder.is_dir():
            total_folders += 1
            print(f"\n正在处理文件夹: {folder.name}")
            
            # 使用集合来避免重复文件
            image_files_set = set()
            for ext in image_extensions:
                for img_file in folder.glob(f"*{ext}"):
                    image_files_set.add(img_file)
                for img_file in folder.glob(f"*{ext.upper()}"):
                    image_files_set.add(img_file)
            
            # 转换为列表并排序
            image_files = list(image_files_set)
            
            # 如果没有找到图片，跳过此文件夹
            if not image_files:
                print(f"  文件夹 {folder.name} 中没有找到支持的图片文件")
                continue
            
            # 使用自然排序算法对图片文件进行排序
            image_files.sort(key=natural_sort_key)
            
            # 打印找到的图片数量
            print(f"  找到 {len(image_files)} 张图片")
            
            # 设置输出PDF路径（在输出目录中，添加前缀）
            pdf_path = output_dir / f"{pdf_prefix}{folder.name}.pdf"
            
            try:
                # 使用img2pdf库转换图片为PDF
                with open(pdf_path, "wb") as f:
                    image_paths = [str(img) for img in image_files]
                    f.write(img2pdf.convert(image_paths))
                
                print(f"  已成功创建: {pdf_path.name}")
                converted_folders += 1
                
            except Exception as e:
                print(f"  转换失败: {e}")
    
    # 打印总结信息
    print("\n" + "="*50)
    print(f"处理完成! 共扫描 {total_folders} 个文件夹，成功转换 {converted_folders} 个文件夹")
    print(f"所有PDF文件已保存到: {output_dir}")
    print(f"PDF文件前缀: {pdf_prefix}")
    print("="*50)

if __name__ == "__main__":
    print("图片转PDF批量处理工具")
    print("所有PDF文件将集中保存到指定输出文件夹，并添加统一前缀")
    print()
    
    # 执行转换
    convert_images_to_pdf()
    
    # 等待用户按键退出
    input("\n按回车键退出...")