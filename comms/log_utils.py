import logging
from comms.constants import INFO_FILE, ERROR_FILE


def get_logger():
    # 第二步：创建日志对象
    logger = logging.getLogger()
    logger.setLevel('DEBUG')  # 代表获取DEBUG及DEBUG级别以上的内容

    # 第三步：设置输出方向
    sh1 = logging.StreamHandler()
    sh1.setLevel('INFO')  # 代表获取INFO及INFO级别以上的内容

    sh2 = logging.FileHandler(filename=INFO_FILE, mode='a', encoding='utf-8')
    sh2.setLevel('INFO')

    sh3 = logging.FileHandler(filename=ERROR_FILE, mode='a', encoding='utf-8')
    sh3.setLevel("ERROR")

    logger.addHandler(sh1)
    logger.addHandler(sh2)
    logger.addHandler(sh3)

    fmt_str = '%(asctime)s - [%(filename)s - %(lineno)d] - %(levelname)s:%(message)s'
    my_fmt = logging.Formatter(fmt_str)
    sh1.setFormatter(my_fmt)
    sh2.setFormatter(my_fmt)
    sh3.setFormatter(my_fmt)
    return logger


logger = get_logger()