try:
    from .logger_config import *
except ImportError as import_error:
    print(import_error.msg)
    print("Please make sure that correct version of file/path exists.")
    exit()
except Exception as e:
    print(e)
    print("Some problem with file Import, make sure correct version of files exists in directory.")
    exit()
