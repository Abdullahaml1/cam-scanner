import numpy as np
from PIL import Image
import argparse
import glob
import os
import cv2



def convert_image_to_printable(img, threshold=120):
    """
    coverts image to gray scale with only two valus (0, 255)
    :param: img (str)
    :param threshold: (number)
    :return : PIL.Image object
    """
    # convert to grayscale
    img = Image.open(img).convert('L')
    img_arr = np.array(img)

    for i in range(img_arr.shape[0]):
        for j in range(img_arr.shape[1]):
            if img_arr[i][j] < threshold:
                img_arr[i][j] = 0 # make it black
            else:
                img_arr[i][j] = 255
            
    return Image.fromarray(img_arr, 'L')



def blur_and_threshold(gray, threshold_blocksize):
    gray = cv2.GaussianBlur(gray,(3,3),2)
    threshold = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, threshold_blocksize, 2)
    threshold = cv2.fastNlMeansDenoising(threshold, 11, 31, 9)
    return threshold

def increase_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    print(hsv)
    h, s, v = cv2.split(hsv)
    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value
    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img  


# **Sharpen the image using Kernel Sharpening Technique**


def final_image(rotated):
  # Create our shapening kernel, it must equal to one eventually
  kernel_sharpening = np.array([[0,-1,0], 
                                [-1, 5,-1],
                                [0,-1,0]])
  # applying the sharpening kernel to the input image & displaying it.
  sharpened = cv2.filter2D(rotated, -1, kernel_sharpening)
  # sharpened=increase_brightness(sharpened,30)  
  return sharpened



def opencv_get_printable(image_path, threshold_blocksize):
    image = cv2.imread(image_path)
    image=image.copy()  
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    threshold_img = blur_and_threshold(gray, threshold_blocksize)
    out_img = final_image(threshold_img)
    return out_img




if __name__=='__main__':
    argparser = argparse.ArgumentParser()

    argparser.add_argument("--threshold", help="threshold to set black and wight",
                           type=int, default=120, required=False)
    argparser.add_argument("--image", help="path to image",
                           type=str, default='', required=False)
    argparser.add_argument("--dir", help="directory to images",
                           type=str, default='', required=False)
    argparser.add_argument("--ext", help="the extention of the images ex: 'jpeg' ",
                           type=str, default='jpeg', required=False)
    argparser.add_argument("--new_name", help="will suffix the name with new_name",
                           type=str, default='print', required=False)
    argparser.add_argument("--rearrange", help="will rename images:1, 2,...",
                           type=str, default='no', required=False)
    argparser.add_argument("--algorithm", help="{normal, adpat}",
                           type=str, default='normal', required=False)
    argparser.add_argument("--adapt_threshold_blocksize", help="{3, 5, 7}",
                           type=int, default=7, required=False)

    args = argparser.parse_args()

    if args.rearrange=='yes':
        images = glob.glob(f'{args.dir}/*.{args.ext}')
        i = .001
        for img in sorted(images):
            new_path = img.split('.')
            new_path = f'{args.dir}/{str(i)[2:5]}.{new_path[-1]}'
            os.rename(img, new_path)
            i += .001


    
    if args.image != '':
        if args.algorithm=='normal':
            img = convert_image_to_printable(args.image, args.threshold)
            new_path = args.image.split('.')
            new_path = f'{".".join(new_path[:-1])}_{args.new_name}.{new_path[-1]}'
            img.save(new_path)

        elif args.algorithm=='adapt':
            out_img = opencv_get_printable(args.image, args.adapt_threshold_blocksize)
            new_path = args.image.split('.')
            new_path = f'{".".join(new_path[:-1])}_{args.new_name}.{new_path[-1]}'
            cv2.imwrite(new_path, out_img)

    # old PIL
    if args.dir != '':
        if args.algorithm=='normal':
            images = glob.glob(f'{args.dir}/*.{args.ext}')
            i=1
            for img in sorted(images):
                print(f'processing <image{i}/{len(images)}>:- {img}')
                new_img = convert_image_to_printable(img, args.threshold)
                new_path = img.split('.')
                new_path = f'{".".join(new_path[:-1])}_{args.new_name}.{new_path[-1]}'
                new_img.save(new_path)
                i +=1

        elif args.algorithm=='adapt':
            images = glob.glob(f'{args.dir}/*.{args.ext}')
            i=1
            for img in sorted(images):
                print(f'processing <image{i}/{len(images)}>:- {img}')
                new_img = opencv_get_printable(img, args.adapt_threshold_blocksize)
                new_path = img.split('.')
                new_path = f'{".".join(new_path[:-1])}_{args.new_name}.{new_path[-1]}'
                cv2.imwrite(new_path, new_img)
                i +=1




