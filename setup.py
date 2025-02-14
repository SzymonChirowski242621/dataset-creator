import os

if __name__ == '__main__':
    if not os.path.exists('images'):
        os.makedirs('images')
        os.makedirs('images/png')

    if not os.path.exists('images/png'):
        os.makedirs('images/png')

    if not os.path.exists('images_out'):
        os.makedirs('images_out')