import os

def get_static_file_path(*sub_paths):
    """
    功能：获取static目录下文件的绝对路径，并自动创建文件所在的目录（多级目录也会创建）
    参数：*sub_paths - 可变参数，传入static下的子路径，例如：
          - 保存图片：
          - 保存txt：
          - 保存csv：
    返回：文件的绝对路径（字符串）
    """
    #获取当前工具文件的绝对路径
    current_file = os.path.abspath(__file__)
    #向上两级目录：utils/ → 项目根目录（7后端/）
    #    如果路径层级不对，可调整os.path.dirname的次数，比如多写一次就是向上三级
    root_dir = os.path.dirname(os.path.dirname(current_file))
    #拼接项目根目录 + static + 子路径
    static_file_path = os.path.join(root_dir, "static", *sub_paths)
    #获取文件所在的目录
    static_dir = os.path.dirname(static_file_path)
    #自动创建目录
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)  # makedirs支持创建多级目录，mkdir只能创建单级
    #返回最终的文件绝对路径
    return static_file_path


if __name__ == "__main__":
    # 测试获取图片路径
    img_path = get_static_file_path("unImg", "月季.jpg")
    print("图片保存路径：", img_path)
    # 测试获取txt路径
    txt_path = get_static_file_path("unSeek", "植物数据.txt")
    print("TXT保存路径：", txt_path)