# =============================================================================
from PIL import Image
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import task2_batch
import task3_net
import os
import pandas as pd
# =======================================================================
# 获取一张图片
#def get_one_image(train):
    # 输入参数：train,训练图片的路径
    # 返回参数：image，从训练图片中随机抽取一张图片
    #n = len(train)
    #ind = np.random.randint(0, n)
    #img_dir = train[ind]  # 随机选择测试的图片

    #img = Image.open(img_dir)
    #plt.imshow(img)
    #imag = img.resize([64, 64])  # 由于图片在预处理阶段以及resize，因此该命令可略
    #image = np.array(imag)
    #return image


def get_one_image(img_dir):
    img = Image.open(img_dir)
    plt.imshow(img)
    imag = img.resize([64, 64])
    image = np.array(imag)
    return image


# --------------------------------------------------------------------
# 测试图片
def evaluate_one_image(image_array):
    with tf.Graph().as_default():
        BATCH_SIZE = 1
        N_CLASSES = 4

        image = tf.cast(image_array, tf.float32)
        image = tf.image.per_image_standardization(image)
        image = tf.reshape(image, [1, 64, 64, 3])

        logit = task3_net.inference(image, BATCH_SIZE, N_CLASSES)

        logit = tf.nn.softmax(logit)

        x = tf.placeholder(tf.float32, shape=[64, 64, 3])

        # you need to change the directories to yours.
        logs_train_dir = 'dataset/log/'

        saver = tf.train.Saver()

        with tf.Session() as sess:

            # print("Reading checkpoints...")
            ckpt = tf.train.get_checkpoint_state(logs_train_dir)
            if ckpt and ckpt.model_checkpoint_path:
                global_step = ckpt.model_checkpoint_path.split('/')[-1].split('-')[-1]
                saver.restore(sess, ckpt.model_checkpoint_path)
                # print('Loading success, global_step is %s' % global_step)
            else:
                print('No checkpoint file found')

            prediction = sess.run(logit, feed_dict={x: image_array})
            # print(prediction)
            # max_index = np.argmax(prediction)
            # if max_index == 0:
            #     print('It is a "Graphic Ringer Tee"')
            # elif max_index == 1:
            #     print('It is a "Sheer Pleated Front Blouse"')
            # elif max_index == 2:
            #     print('It is a "Sheer Sequin Tank"')
            # else:
            #     print('It is a "Single Button Blazer"')
            return prediction[0]



# ------------------------------------------------------------------------

if __name__ == '__main__':
    # test_dir = 'data/数据库男装/数据库男装图片'
    # data = os.walk(test_dir)
    # for root, dirs, files in data:
    #     if len(files) != 0:
    #         # print(root)
    #         # print(dirs)
    #         # print(files)
    #         all_attrs = []
    #         for file in files:
    #             my_dic = {}
    #             img = get_one_image(root+os.sep+file)
    #             attr = evaluate_one_image(img)
    #             my_dic["name"] = file
    #             my_dic["Graphic Ringer Tee"] = attr[0]
    #             my_dic["Sheer Pleated Front Blouse"] = attr[1]
    #             my_dic["Sheer Sequin Tank"] = attr[2]
    #             my_dic["Single Button Blazer"] = attr[3]
    #             all_attrs.append(my_dic)
    #         pd_data = pd.DataFrame(all_attrs)
    #         pd_data.to_csv(root+os.sep+"分类数据.csv", index=False)
    img = get_one_image('data/1.png')
    evaluate_one_image(img)
# ===========================================================================

