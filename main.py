import os
from PIL import Image
import matplotlib.pyplot as plt
import shutil

source_directory = 'images'
target_directory = 'images_out'

def check_images():
    images = [f for f in os.listdir(source_directory) if f.endswith('.png') or f.endswith('.jpg') or f.endswith('.jpeg')]
    if len(images) == 0:
        print('No images found in the images folder')
        exit()
    return images

def check_images_type():
    images = check_images()
    for image in images:
        filename, extension = os.path.splitext(image)
        if extension != '.png':
            convert_image_type(image, 'png')

def convert_image_type(image_path, target_type='png'):
    try:
        if not os.path.exists(f'{source_directory}/png'):
            os.mkdir(f'{source_directory}/png')
        filename, extension = os.path.splitext(image_path)
        im = Image.open(f'{source_directory}/{image_path}')
        im.save(f'{source_directory}/png/{filename}.{target_type}')
    except OSError as e:
        print(f'Error converting image: {e}')

def check_alpha_channel(image_path):
    try:
        im = Image.open(image_path)
        if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
            # Remove alpha channel
            im = im.convert('RGB')
            im.save(image_path)
            return True
        return False
    except OSError as e:
        print(f'Error checking alpha channel: {e}')
        return False

def check_alpha_channel_in_directory(directory):
    images = [f for f in os.listdir(directory) if f.endswith('.png')]
    for image in images:
        image_path = os.path.join(directory, image)
        if check_alpha_channel(image_path):
            print(f'{image_path} had an alpha channel and it was removed')

def get_classes():
    try:
        num_classes = int(input("Enter the number of classes: "))
        class_names = []
        for i in range(num_classes):
            class_name = input(f"Enter the name of class {i + 1}: ")
            class_names.append(class_name)

        class_names.append('not_usable')
        class_names = [class_name.lower() for class_name in class_names]
        return class_names
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return []

def classify_images(class_names):
    images = [f for f in os.listdir(f'{source_directory}/png') if f.endswith('.png')]
    image_class_mapping = {}

    for image in images:
        image_path = os.path.join(f'{source_directory}/png', image)
        im = Image.open(image_path)
        plt.imshow(im)
        plt.title(f"Image: {image}")
        plt.axis('off')
        plt.show()

        for idx, class_name in enumerate(class_names):
            print(f"{idx + 1}. {class_name}")

        while True:
            try:
                class_index = int(input("Select the class number for this image: ")) - 1
                if 0 <= class_index < len(class_names):
                    image_class_mapping[image] = class_names[class_index]
                    break
                else:
                    print("Invalid class number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    return image_class_mapping

def create_class_folders_and_move_images(image_class_mapping, class_names):
    for class_name in class_names:
        class_folder = os.path.join(target_directory, class_name)
        if not os.path.exists(class_folder):
            os.makedirs(class_folder)

    for image, class_name in image_class_mapping.items():
        src_path = os.path.join(f'{source_directory}/png', image)
        dst_path = os.path.join(target_directory, class_name, image)
        shutil.move(src_path, dst_path)

def show_statistics():
    def count_images_in_folder(folder):
        class_counts = {}
        for class_name in os.listdir(folder):
            class_folder = os.path.join(folder, class_name)
            if os.path.isdir(class_folder):
                class_counts[class_name] = len(os.listdir(class_folder))
        return class_counts

    train_counts = count_images_in_folder(target_directory)

    print("\nStatistics:")
    print(f"Total images: {sum(train_counts.values())} images")
    for class_name, count in train_counts.items():
        print(f"  {class_name}: {count} images")

if __name__ == '__main__':
    images = check_images()
    check_images_type()
    check_alpha_channel_in_directory(f'{source_directory}/png')
    class_names = get_classes()
    print(f"Class names: {class_names}")
    image_class_mapping = classify_images(class_names)
    print(f"Image classifications: {image_class_mapping}")
    create_class_folders_and_move_images(image_class_mapping, class_names)
    print("Images have been moved to their respective class folders.")
    show_statistics()