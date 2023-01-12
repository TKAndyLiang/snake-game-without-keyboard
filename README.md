# Snake-game-without-keyboard

### We provide four methods to implement this project.
>The project enviroment is under python version 3.9.15 with pytorch version 1.11.3 and CUDA version 11.3.
>Please install the project dependency first.
```shell
pip install torch==1.11.0+cu113 torchvision==0.12.0+cu113 torchaudio==0.11.0 --extra-index-url https://download.pytorch.org/whl/cu113
pip install -r requirements.txt
```
The detail discription for those methods can be viewed at this [link][7].
<br/><br/>
For mehtod three and method four, you need to download the model weight in order to run the code, which can be download here: [link][1](for method three) and [link][2](for method four).

### How to run our code
+ Pleace wait until both the cv2 window and the gaming window show up, then click on the gaming window, the game will be ready to receive the signal.
+ Make sure which camera you are using. If the cv2 window is all black or not correctly show up, the argument command **``-c``** can change the camera device on your desktop(default 0).

<br/>

+ For method one [demo video][3]
```shell
python run.py -m yuan -c 0
```
+ For method two [demo video][4]
```shell
python run_du.py -m direct -c 0
```
+ For method three [demo video][5]
```shell
python run_du.py -m model -c 0
```
+ For method four [demo video][6]
```shell
python run.py -m yao -c 0
```

[1]: https://drive.google.com/file/d/1piKJIC01_I6YVz0juqCiy3kJXS4JDZhx/view?usp=share_link
[2]: https://drive.google.com/file/d/1OAMp327bKV47KRWz5aL9YpPZnS0RYQvE/view?usp=share_link
[3]: https://youtu.be/fEIULEbItR0
[4]: https://youtu.be/Uqw-957p3hk
[5]: https://youtu.be/j_IDteFhxGU
[6]: https://youtu.be/gAEc_gp_bGc
[7]: https://drive.google.com/file/d/1UEwYTjcsMonzC_oL_fLPpojRyGL4kIIg/view?usp=share_link
