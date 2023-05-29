# cam-scanner
This is a simple command line cam-scanner tool:
* **input**: colored image
* **Output**: gray scale with (black=0, white=255) only to be printed with black and white printer

The script has two methods:
* **normal**: which uses a fixed threshold to generate balck and white text
* **adapt**: Using opencv adaptive threshold which calculate threshold every block size 

## Prerquisites
```
pip install opencv-python
```

## Noraml method
### Single image

```
python3 generate_printable_image.py --image='your image path' --ext={jpg, jpeg, png, ...} --algorithm=noraml --threshold={form 0 to 255, prefared 135}

```
The output is the same image affixes with `print`, Ex: `--image=test.jpg, output=test_print.jpg`

**Example**
```
python3 generate_printable_image.py --image=docdoc.jpg --ext=jpg --algorithm=normal --threshold=135
```


### Dirctory of images

```
python3 generate_printable_image.py --dir='the directory with your images with ext' --ext={jpg, jpeg, png, ...} --algorithm=noraml --threshold={form 0 to 255, prefared 135}

```
The output is the same images' name in the dirctory affixes with `print`. Ex:
```
./tes_dir/
	img1.png
	img2.png
	img3.png
	img4.png
```
Ouput:
```
./tes_dir/
	img1.png
	img1_print.png
	img2.png
	img2_print.png
	img3.png
	img3_print.png
	img4.png
	img4_print.png
```

**Example**:

```
python3 generate_printable_image.py --dir=MennaPrint --ext=jpg --algorithm=normal --threshold=132
```


## Adapt method
Using opencv adaptive threshold, which computes the threshold every block size.
We can control the block size using `----adapt_threshold_blocksize=`
### Single image

```
python3 generate_printable_image.py --image='your image path' --ext={jpg, jpeg, png, ...} --algorithm=adapt --adapt_threshold_blocksize={3, 5, 7, .. more block size more black dots}
```
The output is the same image affixes with `print`, Ex: `--image=test.jpg, output=test_print.jpg`

**Example**
```
python3 generate_printable_image.py --image=doc.jpeg --ext=jpeg --algorithm=adapt --adapt_threshold_blocksize=7
```


### Dirctory of images

```
python3 generate_printable_image.py --dir='the directory with your images with ext' --ext={jpg, jpeg, png, ...} --algorithm=adapt --adapt_threshold_blocksize={3, 5, 7, .. more block size more black dots}
```
The output is the same images' name in the dirctory affixes with `print`. Ex:
```
./tes_dir/
	img1.png
	img2.png
	img3.png
	img4.png
```
Ouput:
```
./tes_dir/
	img1.png
	img1_print.png
	img2.png
	img2_print.png
	img3.png
	img3_print.png
	img4.png
	img4_print.png
```

**Example**:

```
python3 generate_printable_image.py --dir=../Downloads/print4 --ext=jpg --algorithm=adapt --adapt_threshold_blocksize=7
```

# Resources
* opencv mehtod [link](https://levelup.gitconnected.com/create-your-own-camscanner-using-python-opencv-2dd8355432de)
