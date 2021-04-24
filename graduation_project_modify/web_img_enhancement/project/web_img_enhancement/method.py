import cv2
import numpy as np
from math import exp,pow

def cv_imread(file_path):
    cv_img = cv2.imdecode(np.fromfile(file_path,dtype=np.uint8),-1)
    return cv_img

#定义去0防止出现转为对数时溢出
def removeZeroes(src):
    min_not0 = min(src[np.nonzero(src)])
    src[src == 0] = min_not0
    return src

#计算lamda
def cal_lamda(x,y,c):
    sum = 0
    for i in range(x):
        for j in range(y):
            sum = sum + exp(-(pow(i,2)+pow(j,2))/pow(c,2))
    lamda = 1/sum
    return lamda

#计算函数F
def cal_F(x,y,lamda,c):
    F = np.zeros((x,y),np.float32)
    for i in range(x):
        for j in range(y):
            F[i,j] = lamda * exp(-(pow(i,2)+pow(j,2))/pow(c,2))
    return F

#计算卷积
def cal_conv(A,B):
    A_fre = np.fft.fft2(A)
    A_fre_shift = np.fft.fftshift(A_fre)
    B_fre = np.fft.fft2(B)
    B_fre_shift = np.fft.fftshift(B_fre)
    AB_fre_shift = B_fre_shift * A_fre_shift
    AB_fre = np.fft.ifftshift(AB_fre_shift)
    AB = np.fft.ifft2(AB_fre)
    AB = np.real(AB)
    return AB

def Msrcr_stretch(img,Dynamic):
    Mean = np.mean(img)
    Var  = np.std(img)
    img_min = Mean - Dynamic * Var
    img_max = Mean + Dynamic * Var
    img = (img - img_min) * 255 / (img_max - img_min)
    img[img>255] = 255
    img[img<0] = 0
    return img

def msrcr(name,resname):
    print(name)
    img = cv_imread(name)
    img = removeZeroes(img)
    r,c = img.shape[:2]
    f = []
    #F1
    lamda = cal_lamda(r,c,15)
    F1 = cal_F(r,c,lamda,15)
    F1 = removeZeroes(F1)
    f.append(F1)

    #F2
    lamda = cal_lamda(r,c,80)
    F2 = cal_F(r,c,lamda,80)
    F2 = removeZeroes(F2)
    f.append(F2)

    #F3
    lamda = cal_lamda(r,c,200)
    F3 = cal_F(r,c,lamda,200)
    F3 = removeZeroes(F3)
    f.append(F3)

    img = img.astype(np.float32)
    B = img[:,:,0]
    G = img[:,:,1]
    R = img[:,:,2]
    B_log = np.log(B)
    G_log = np.log(G)
    R_log = np.log(R)

    r_B=0
    r_G=0
    r_R=0
    w = [0.333,0.333,0.334]

    for i in range(3):
        r_B = r_B + w[i] * (B_log - np.log(abs(cal_conv(B, f[i]))))
        r_G = r_G + w[i] * (G_log - np.log(abs(cal_conv(G, f[i]))))
        r_R = r_R + w[i] * (R_log - np.log(abs(cal_conv(R, f[i]))))

    #MSRCR量化操作
    result_B = Msrcr_stretch(r_B,2.5)
    result_G = Msrcr_stretch(r_G,2.5)
    result_R = Msrcr_stretch(r_R,2.5)

    #转为uint8
    result_B = np.uint8(result_B)
    result_G = np.uint8(result_G)
    result_R = np.uint8(result_R)
    result = cv2.merge([result_B,result_G,result_R])
    cv2.imencode('.jpg', result)[1].tofile(resname)
    cv2.waitKey()

def agcwd(image, w=0.5):
    is_colorful = len(image.shape) >= 3
    img = extract_value_channel(image) if is_colorful else image
    img_pdf = get_pdf(img)
    max_intensity = np.max(img_pdf)
    min_intensity = np.min(img_pdf)
    w_img_pdf = max_intensity * (((img_pdf - min_intensity) / (max_intensity - min_intensity)) ** w)
    w_img_cdf = np.cumsum(w_img_pdf) / np.sum(w_img_pdf)
    l_intensity = np.arange(0, 256)
    l_intensity = np.array([255 * (e / 255) ** (1 - w_img_cdf[e]) for e in l_intensity], dtype=np.uint8)
    enhanced_image = np.copy(img)
    height, width = img.shape
    for i in range(0, height):
        for j in range(0, width):
            intensity = enhanced_image[i, j]
            enhanced_image[i, j] = l_intensity[intensity]
    enhanced_image = set_value_channel(image, enhanced_image) if is_colorful else enhanced_image
    return enhanced_image


def extract_value_channel(color_image):
    color_image = color_image.astype(np.float32) / 255.
    hsv = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)
    v = hsv[:, :, 2]
    return np.uint8(v * 255)


def get_pdf(gray_image):
    height, width = gray_image.shape
    pixel_count = height * width
    hist = cv2.calcHist([gray_image], [0], None, [256], [0, 256])
    return hist / pixel_count


def set_value_channel(color_image, value_channel):
    value_channel = value_channel.astype(np.float32) / 255
    color_image = color_image.astype(np.float32) / 255.
    color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)
    color_image[:, :, 2] = value_channel
    color_image = np.array(cv2.cvtColor(color_image, cv2.COLOR_HSV2BGR) * 255, dtype=np.uint8)
    return color_image

def zmMinFilterGray(src, r=7):
    '''最小值滤波，r是滤波器半径'''
    '''if r <= 0:
      return src
  h, w = src.shape[:2]
  I = src
  res = np.minimum(I  , I[[0]+range(h-1)  , :])
  res = np.minimum(res, I[range(1,h)+[h-1], :])
  I = res
  res = np.minimum(I  , I[:, [0]+range(w-1)])
  res = np.minimum(res, I[:, range(1,w)+[w-1]])
  return zmMinFilterGray(res, r-1)'''
    return cv2.erode(src, np.ones((2 * r + 1, 2 * r + 1)))  # 使用opencv的erode函数更高效


def guidedfilter(I, p, r, eps):
    '''引导滤波，直接参考网上的matlab代码'''
    height, width = I.shape
    m_I = cv2.boxFilter(I, -1, (r, r))
    m_p = cv2.boxFilter(p, -1, (r, r))
    m_Ip = cv2.boxFilter(I * p, -1, (r, r))
    cov_Ip = m_Ip - m_I * m_p

    m_II = cv2.boxFilter(I * I, -1, (r, r))
    var_I = m_II - m_I * m_I

    a = cov_Ip / (var_I + eps)
    b = m_p - a * m_I

    m_a = cv2.boxFilter(a, -1, (r, r))
    m_b = cv2.boxFilter(b, -1, (r, r))
    return m_a * I + m_b


def getV1(m, r, eps, w, maxV1):  # 输入rgb图像，值范围[0,1]
    '''计算大气遮罩图像V1和光照值A, V1 = （1-t）A'''
    V1 = np.min(m, 2)  # 得到暗通道图像
    V1 = guidedfilter(V1, zmMinFilterGray(V1, 7), r, eps)  # 使用引导滤波优化
    bins = 2000
    ht = np.histogram(V1, bins)  # 计算大气光照A
    d = np.cumsum(ht[0]) / float(V1.size)
    for lmax in range(bins - 1, 0, -1):
        if d[lmax] <= 0.999:
            break
    A = np.mean(m, 2)[V1 >= ht[1][lmax]].max()

    V1 = np.minimum(V1 * w, maxV1)  # 对值范围进行限制

    return V1, A


def deHaze(m, r=81, eps=0.001, w=0.95, maxV1=0.80, bGamma=False):
    Y = np.zeros(m.shape)
    V1, A = getV1(m, r, eps, w, maxV1)  # 得到遮罩图像和大气光照
    for k in range(3):
        Y[:, :, k] = (m[:, :, k] - V1) / (1 - V1 / A)  # 颜色校正
    Y = np.clip(Y, 0, 1)
    if bGamma:
        Y = Y ** (np.log(0.5) / np.log(Y.mean()))  # gamma校正,默认不进行该操作
    return Y


def AGCWD(name,resname):
    img = cv_imread(name)
    result = agcwd(img)
    cv2.imencode('.jpg', result)[1].tofile(resname)
    cv2.waitKey()

def quwu(name,resname):
    result = deHaze(cv_imread(name) / 255.0) * 255
    cv2.imencode('.jpg', result)[1].tofile(resname)
    cv2.waitKey()

def enhanced_reinhard(src_img: np.ndarray, ref_img: np.ndarray):
    src_img = src_img.astype(np.float64)
    ref_img = ref_img.astype(np.float64)
    res_img = src_img.copy()
    src_l, src_alpha, src_beta = src_img[:, :, 0], src_img[:, :, 1], src_img[:, :, 2]
    ref_l, ref_alpha, ref_beta = ref_img[:, :, 0], ref_img[:, :, 1], ref_img[:, :, 2]

    # reinhard
    res_img[:, :, 0] -= np.mean(src_l)
    res_img[:, :, 1] -= np.mean(src_alpha)
    res_img[:, :, 2] -= np.mean(src_beta)

    res_img[:, :, 0] *= np.std(ref_l) / np.std(src_l)
    res_img[:, :, 1] *= np.std(ref_alpha) / np.std(src_alpha)
    res_img[:, :, 2] *= np.std(ref_beta) / np.std(src_beta)

    res_img[:, :, 0] += np.mean(ref_l)
    res_img[:, :, 1] += np.mean(ref_alpha)
    res_img[:, :, 2] += np.mean(ref_beta)

    # 处理过曝
    # 三通道处理过曝，效果并不好
    # enhance_rate = src_img.copy()
    # enhance_rate[:, :, 0] = src_img[:, :, 0] / np.exp(src_img[:, :, 0] / np.mean(src_img[:, :, 0]))
    # enhance_rate[:, :, 1] = src_img[:, :, 1] / np.exp(src_img[:, :, 1] / np.mean(src_img[:, :, 1]))
    # enhance_rate[:, :, 2] = src_img[:, :, 2] / np.exp(src_img[:, :, 2] / np.mean(src_img[:, :, 2]))
    # 整体

    # enhance_rate = np.power(src_img, pow_num) / np.exp(src_img / np.mean(src_img) * pow_num)
    # enhance_rate /= np.max(enhance_rate) / max_enhance_rate
    # res_img = (res_img - src_img) * enhance_rate + src_img

    res_img[res_img > 255] = 255
    res_img[res_img < 0] = 0
    return res_img.astype(np.uint8)

def getVarianceMean(scr, winSize):
    if scr is None or winSize is None:
        print("The input parameters of getVarianceMean Function error")
        return -1

    if winSize % 2 == 0:
        print("The window size should be singular")
        return -1

    copyBorder_map = cv2.copyMakeBorder(scr, winSize // 2, winSize // 2, winSize // 2, winSize // 2,
                                        cv2.BORDER_REPLICATE)
    shape = np.shape(scr)

    local_mean = np.zeros_like(scr)
    local_std = np.zeros_like(scr)

    for i in range(shape[0]):
        for j in range(shape[1]):
            temp = copyBorder_map[i:i + winSize, j:j + winSize]
            local_mean[i, j], local_std[i, j] = cv2.meanStdDev(temp)
            if local_std[i, j] <= 0:
                local_std[i, j] = 1e-8

    return local_mean, local_std


def adaptContrastEnhancement(scr, winSize, maxCg):
    if scr is None or winSize is None or maxCg is None:
        print("The input parameters of ACE Function error")
        return -1

    YUV_img = cv2.cvtColor(scr, cv2.COLOR_BGR2YUV)  ##转换通道
    Y_Channel = YUV_img[:, :, 0]
    shape = np.shape(Y_Channel)

    meansGlobal = cv2.mean(Y_Channel)[0]

    ##这里提供使用boxfilter 计算局部均质和方差的方法
    #    localMean_map=cv2.boxFilter(Y_Channel,-1,(winSize,winSize),normalize=True)
    #    localVar_map=cv2.boxFilter(np.multiply(Y_Channel,Y_Channel),-1,(winSize,winSize),normalize=True)-np.multiply(localMean_map,localMean_map)
    #    greater_Zero=localVar_map>0
    #    localVar_map=localVar_map*greater_Zero+1e-8
    #    localStd_map = np.sqrt(localVar_map)

    localMean_map, localStd_map = getVarianceMean(Y_Channel, winSize)

    for i in range(shape[0]):
        for j in range(shape[1]):

            cg = 0.2 * meansGlobal / localStd_map[i, j];
            if cg > maxCg:
                cg = maxCg
            elif cg < 1:
                cg = 1

            temp = Y_Channel[i, j].astype(float)
            temp = max(0, min(localMean_map[i, j] + cg * (temp - localMean_map[i, j]), 255))

            #            Y_Channel[i,j]=max(0,min(localMean_map[i,j]+cg*(Y_Channel[i,j]-localMean_map[i,j]),255))
            Y_Channel[i, j] = temp

    YUV_img[:, :, 0] = Y_Channel

    dst = cv2.cvtColor(YUV_img, cv2.COLOR_YUV2BGR)

    return dst

def gauss_blur(img, ksize, sigma):
    '''
    高斯模糊
    :param img: 原始图片
    :param ksize: 高斯内核大小。 ksize.width和ksize.height可以不同，但​​它们都必须为正数和奇数，也可以为零
    :param sigma: 标准差，如果写0，则函数会自行计算
    :return:
    '''
    # 外部调用传入正整数即可,在这里转成奇数
    k_list = list(ksize)
    kw = (k_list[0] * 2) + 1
    kh = (k_list[1] * 2) + 1
    resultImg = cv2.GaussianBlur(img, (kw, kh), sigma)
    return resultImg

def lashen(name,resname):
    img = cv_imread(name)
    res_img = adaptContrastEnhancement(img, 15, 10)
    cv2.imencode('.jpg', np.uint8(res_img))[1].tofile(resname)
    cv2.waitKey()

def jiami(name,resname):
    pass

def mohu(name,resname):
    img = cv_imread(name)
    res_img = gauss_blur(img, (7, 7), 0)
    cv2.imencode('.jpg', np.uint8(res_img))[1].tofile(resname)
    cv2.waitKey()

def cv_filter2d(src):

    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])

    dst = cv2.filter2D(src, -1, kernel)

    return dst

def ruihua(name,resname):
    img = cv_imread(name)
    res_img = cv_filter2d(img)
    cv2.imencode('.jpg', np.uint8(res_img))[1].tofile(resname)
    cv2.waitKey()



def shibie(name,resname):
    img = cv_imread(name)
    img = cv2.GaussianBlur(img, (3, 3), 0)
    canny = cv2.Canny(img, 50, 150)
    cv2.imencode('.jpg', np.uint8(canny))[1].tofile(resname)
    cv2.waitKey()

def quzao(name,resname):
    img = cv_imread(name)
    result = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
    cv2.imencode('.jpg', np.uint8(result))[1].tofile(resname)
    cv2.waitKey()

def trans(yuanname,canzhaoname,resname):
    src_img = cv_imread(yuanname)
    src_img = cv2.cvtColor(src_img, cv2.COLOR_BGR2LAB)
    ref_img = cv_imread(canzhaoname)
    ref_img = cv2.cvtColor(ref_img, cv2.COLOR_BGR2LAB)

    res_img = enhanced_reinhard(src_img, ref_img)
    res_img = cv2.cvtColor(res_img, cv2.COLOR_LAB2BGR)
    cv2.imencode('.jpg', np.uint8(res_img))[1].tofile(resname)
    cv2.waitKey()