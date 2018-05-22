# _*_ coding: utf-8 _*_

import os
import numpy
import logging
from collections import defaultdict
import pymongo
from nltk import tokenize
import stop_words
from nltk.stem.porter import PorterStemmer
import json

# 全局变量
MAX_ITER_NUM = 10000    # 最大迭代次数
VAR_NUM = 20            # 自动计算迭代次数时,计算方差的区间大小


class BiDictionary(object):
    """
    定义双向字典,通过key可以得到value,通过value也可以得到key
    """

    def __init__(self):
        """
        :key: 双向字典初始化
        """
        self.dict = {}            # 正向的数据字典,其key为self的key
        self.dict_reversed = {}   # 反向的数据字典,其key为self的value
        return

    def __len__(self):
        """
        :key: 获取双向字典的长度
        """
        return len(self.dict)

    def __str__(self):
        """
        :key: 将双向字典转化为字符串对象
        """
        str_list = ["%s\t%s" % (key, self.dict[key]) for key in self.dict]
        return "\n".join(str_list)

    def clear(self):
        """
        :key: 清空双向字典对象
        """
        self.dict.clear()
        self.dict_reversed.clear()
        return

    def add_key_value(self, key, value):
        """
        :key: 更新双向字典,增加一项
        """
        self.dict[key] = value
        self.dict_reversed[value] = key
        return

    def remove_key_value(self, key, value):
        """
        :key: 更新双向字典,删除一项
        """
        if key in self.dict:
            del self.dict[key]
            del self.dict_reversed[value]
        return

    def get_value(self, key, default=None):
        """
        :key: 通过key获取value,不存在返回default
        """
        return self.dict.get(key, default)

    def get_key(self, value, default=None):
        """
        :key: 通过value获取key,不存在返回default
        """
        return self.dict_reversed.get(value, default)

    def contains_key(self, key):
        """
        :key: 判断是否存在key值
        """
        return key in self.dict

    def contains_value(self, value):
        """
        :key: 判断是否存在value值
        """
        return value in self.dict_reversed

    def keys(self):
        """
        :key: 得到双向字典全部的keys
        """
        return self.dict.keys()

    def values(self):
        """
        :key: 得到双向字典全部的values
        """
        return self.dict_reversed.keys()

    def items(self):
        """
        :key: 得到双向字典全部的items
        """
        return self.dict.items()


class CorpusSet(object):
    """
    定义语料集类,作为LdaBase的基类
    """

    def __init__(self):
        """
        :key: 初始化函数
        """
        # 定义关于word的变量
        self.local_bi = BiDictionary()      # id和word之间的本地双向字典,key为id,value为word
        self.words_count = 0                # 数据集中word的数量（排重之前的）
        self.V = 0                          # 数据集中word的数量（排重之后的）

        # 定义关于article的变量
        self.artids_list = []               # 全部article的id的列表,按照数据读取的顺序存储
        self.arts_Z = []                    # 全部article中所有词的id信息,维数为 M * art.length()
        self.M = 0                          # 数据集中article的数量
        self.arts_ref = []  # 全部article中所有参考文献id，M * art.Lm
        self.arts_auth = []  # 全部article中所有作者id，M * art.Am
        self.artconfs_list = []  # 全部article的会议id列表

        # 关于作者author
        self.authorids_list = []  # 全部author的id列表
        self.auths_paper = []  # 全部author的论文id，A * A.p

        # 关于会议conf
        self.confids_list = []  # 全部conf的id列表
        self.confs_paper = []  # 全部conf的论文id，C * C.p

        # 定义推断中用到的变量（可能为空）
        self.global_bi = None               # id和word之间的全局双向字典,key为id,value为word
        self.local_2_global = {}            # 一个字典,local字典和global字典之间的对应关系
        return

    def init_corpus_with_file(self, file_name):
        """
        :key: 利用数据文件初始化语料集数据。文件每一行的数据格式: id[tab]word1 word2 word3......
        """
        with open(file_name, "r", encoding="utf-8") as file_iter:
            self.init_corpus_with_articles(file_iter)
        return

    def init_corpus_with_mongodb(self, ip, port):
        # 清理数据--word数据
        self.local_bi.clear()
        self.words_count = 0
        self.V = 0

        # 清理数据--article数据
        self.artids_list.clear()
        self.arts_Z.clear()
        self.M = 0
        self.arts_ref.clear()
        self.arts_auth.clear()
        self.artconfs_list.clear()

        # 清理数据--author数据
        self.authorids_list.clear()
        self.auths_paper.clear()

        # 清理数据--conf数据
        self.confids_list.clear()
        self.confs_paper.clear()

        # 清理数据--清理local到global的映射关系
        self.local_2_global.clear()

        conn = pymongo.MongoClient(ip, port)
        db = conn.papertest

        # 读取author数据
        mauthor = db.mAuthor
        for line in mauthor.find():
            self.authorids_list.append(str(line['_id']))
            self.auths_paper.append([])

        # 读取conf数据
        mconf = db.mConf
        for line in mconf.find():
            self.confids_list.append(str(line['_id']))
            self.confs_paper.append([])

        # 读取article数据
        mpaper = db.mPaper
        pattern = r"""(?x)                   # set flag to allow verbose regexps
                      (?:[A-Z]\.)+           # abbreviations, e.g. U.S.A.
                      |\d+(?:\.\d+)?%?       # numbers, incl. currency and percentages
                      |\w+(?:[-']\w+)*       # words w/ optional internal hyphens/apostrophe
                    """
        tokenizer = tokenize.RegexpTokenizer(pattern)
        en_stop = stop_words.get_stop_words('en')  # stop words
        p_stemmer = PorterStemmer()
        for line in mpaper.find():
            # 获取article的id
            art_id = line['oriid']

            # 获取word的id
            tokens = tokenizer.tokenize(line['abs'])  # 分词
            low_tokens = [w.lower() for w in tokens]  # 转小写
            stopped_tokens = [w for w in low_tokens if w not in en_stop]  # 去除停用词
            stemmed_tokens = [p_stemmer.stem(w) for w in stopped_tokens]  # 词干提取
            art_wordid_list = []
            for word in stemmed_tokens:
                local_id = self.local_bi.get_key(word) if self.local_bi.contains_value(word) else len(self.local_bi)

                # 这里的self.global_bi为None和为空是有区别的
                if self.global_bi is None:
                    # 更新id信息
                    self.local_bi.add_key_value(local_id, word)
                    art_wordid_list.append(local_id)
                else:
                    if self.global_bi.contains_value(word):
                        # 更新id信息
                        self.local_bi.add_key_value(local_id, word)
                        art_wordid_list.append(local_id)

                        # 更新local_2_global
                        self.local_2_global[local_id] = self.global_bi.get_key(word)

            # 更新类变量: 必须article中word的数量大于0
            if len(art_wordid_list) > 0:
                self.words_count += len(art_wordid_list)
                self.artids_list.append(art_id)
                self.arts_Z.append(art_wordid_list)
                # 获取参考文献id
                self.arts_ref.append(json.loads(line['refs']))
                # 获取作者id
                auths = []
                for auth in json.loads(line['authorsid']):
                    aid = self.authorids_list.index(auth)
                    auths.append(aid)
                    self.auths_paper[aid].append(len(self.artids_list) - 1)
                self.arts_auth.append(auths)
                # 获取会议id
                cid = self.confids_list.index(line['vuene'])
                self.artconfs_list.append(cid)
                self.confs_paper[cid].append(len(self.artids_list) - 1)
        for m in range(len(self.artids_list)):
            for r in range(len(self.arts_ref[m])):
                self.arts_ref[m][r] = self.artids_list.index(self.arts_ref[m][r])

        # 做相关初始计算--word相关
        self.V = len(self.local_bi)
        logging.debug("words number: " + str(self.V) + ", " + str(self.words_count))

        # 做相关初始计算--article相关
        self.M = len(self.artids_list)
        logging.debug("articles number: " + str(self.M))

        return

    def init_corpus_with_articles(self, article_list):
        """
        :key: 利用article的列表初始化语料集。每一篇article的格式为: id[tab]word1 word2 word3......
        """
        # 清理数据--word数据
        self.local_bi.clear()
        self.words_count = 0
        self.V = 0

        # 清理数据--article数据
        self.artids_list.clear()
        self.arts_Z.clear()
        self.M = 0

        # 清理数据--清理local到global的映射关系
        self.local_2_global.clear()

        # 读取article数据
        for line in article_list:
            frags = line.strip().split()
            if len(frags) < 2:
                continue

            # 获取article的id
            art_id = frags[0].strip()

            # 获取word的id
            art_wordid_list = []
            for word in [w.strip() for w in frags[1:] if w.strip()]:
                local_id = self.local_bi.get_key(word) if self.local_bi.contains_value(word) else len(self.local_bi)

                # 这里的self.global_bi为None和为空是有区别的
                if self.global_bi is None:
                    # 更新id信息
                    self.local_bi.add_key_value(local_id, word)
                    art_wordid_list.append(local_id)
                else:
                    if self.global_bi.contains_value(word):
                        # 更新id信息
                        self.local_bi.add_key_value(local_id, word)
                        art_wordid_list.append(local_id)

                        # 更新local_2_global
                        self.local_2_global[local_id] = self.global_bi.get_key(word)

            # 更新类变量: 必须article中word的数量大于0
            if len(art_wordid_list) > 0:
                self.words_count += len(art_wordid_list)
                self.artids_list.append(art_id)
                self.arts_Z.append(art_wordid_list)

        # 做相关初始计算--word相关
        self.V = len(self.local_bi)
        logging.debug("words number: " + str(self.V) + ", " + str(self.words_count))

        # 做相关初始计算--article相关
        self.M = len(self.artids_list)
        logging.debug("articles number: " + str(self.M))
        return

    def save_wordmap(self, file_name):
        """
        :key: 保存word字典,即self.local_bi的数据
        """
        with open(file_name, "w", encoding="utf-8") as f_save:
            f_save.write(str(self.local_bi))
        return

    def load_wordmap(self, file_name):
        """
        :key: 加载word字典,即加载self.local_bi的数据
        """
        self.local_bi.clear()
        with open(file_name, "r", encoding="utf-8") as f_load:
            for _id, _word in [line.strip().split() for line in f_load if line.strip()]:
                self.local_bi.add_key_value(int(_id), _word.strip())
        self.V = len(self.local_bi)
        return


class LdaBase(CorpusSet):
    """
    LDA模型的基类,相关说明:
    》article的下标范围为[0, self.M), 下标为 m
    》wordid的下标范围为[0, self.V), 下标为 w
    》topic的下标范围为[0, self.K), 下标为 k 或 topic
    》article中word的下标范围为[0, article.size()), 下标为 n
    """

    def __init__(self):
        """
        :key: 初始化函数
        """
        CorpusSet.__init__(self)

        # 基础变量--1
        self.dir_path = ""          # 文件夹路径,用于存放LDA运行的数据、中间结果等
        self.model_name = ""        # LDA训练或推断的模型名称,也用于读取训练的结果
        self.current_iter = 0       # LDA训练或推断的模型已经迭代的次数,用于继续模型训练过程
        self.iters_num = 0          # LDA训练或推断过程中Gibbs抽样迭代的总次数,整数值或者"auto"
        self.topics_num = 0         # LDA训练或推断过程中的topic的数量,即self.K值
        self.K = 0                  # LDA训练或推断过程中的topic的数量,即self.topics_num值
        self.twords_num = 0         # LDA训练或推断结束后输出与每个topic相关的word的个数

        # 基础变量--2
        self.alpha = numpy.zeros(self.K)            # 超参数alpha,K维的float值,默认为50/K
        self.beta = numpy.zeros(self.V)             # 超参数beta,V维的float值,默认为0.01
        self.eta = [numpy.zeros(len(i)) for i in self.arts_ref]  # 超参数eta, M * Lm
        self.gamma = [numpy.zeros(len(i)) for i in self.arts_auth]  # 超参数gamma, M * Am
        self.alpha_lambda = numpy.zeros(4)  # # 超参数alpha_lambda, 4维

        # 基础变量--3
        self.Z = []                                 # 所有word的topic信息,即Z(m, n),维数为 M * article.size()
        self.S = []  # 所有word的source信息,即S(m, n),维数为 M * article.size()
        self.R = []  # 所有word的ref信息,即R(m, n),维数为 M * article.size()
        self.A = []  # 所有word的author信息,即A(m, n),维数为 M * article.size()
        self.C = []  # 所有word的paper-conf信息,即C(m, n),维数为 M * article.size()

        # 统计计数(可由self.ZSRAC计算得到)
        self.nd = numpy.zeros((self.M, self.K))     # nd[m, k]用于保存第m篇article的第k个topic产生的词的个数,其维数为 M * K
        self.ndsum = numpy.zeros((self.M, 1))       # ndsum[m, 0]用于保存第m篇article生成的总词数,维数为 M * 1
        self.nw = numpy.zeros((self.K, self.V))     # nw[k, w]用于保存第k个topic产生的词中第w个词的数量,其维数为 K * V
        self.nwsum = numpy.zeros((self.K, 1))       # nwsum[k, 0]用于保存第k个topic产生的词的总数,维数为 K * 1
        self.ns = numpy.zeros((self.M, 4))  # ns[m, i]用于保存第m篇article中来源为i的词的个数,其维数为 M * 4
        self.nr = [numpy.zeros(len(i)) for i in self.arts_ref]  # nr[m][r]用于保存第m篇article中选择参考文献r的词的个数,其维数为 M * Lm
        self.na = [numpy.zeros(len(i)) for i in self.arts_auth]  # na[m][a]用于保存第m篇article中选择作者a的词的个数,其维数为 M * Am
        self.nssum = numpy.zeros((self.K, 1))  # nssum[m, 0]用于保存第m篇article的总词数,维数为 M * 1
        self.an = numpy.zeros((len(self.authorids_list), self.K))  # an[a, k]用于保存第a个author的第k个topic产生的词的个数,其维数为 A * K
        self.ansum = numpy.zeros((len(self.authorids_list), 1))  # ansum[a, 0]用于保存第a个author生成的总词数,维数为 A * 1

        # 多项式分布参数变量
        self.theta = numpy.zeros((self.M, self.K))  # Doc-Topic多项式分布的参数,维数为 M * K,由alpha值影响
        self.phi = numpy.zeros((self.K, self.V))    # Topic-Word多项式分布的参数,维数为 K * V,由beta值影响
        self.delta = [numpy.zeros(len(i)) for i in self.arts_ref]  # Doc-Ref多项式分布的参数,维数为 M * Lm,由eta值影响
        self.mu = [numpy.zeros(len(i)) for i in self.arts_auth]  # Doc-Author多项式分布的参数,维数为 M * Am,由gamma值影响
        self.llambda = numpy.zeros((self.M, 4))  # Doc-Source多项式分布的参数,维数为 M * 4,由alpha_lambda值影响
        self.theta_a = numpy.zeros((len(self.authorids_list), self.K))  # Author-Topic多项式分布的参数,维数为 A * K,由alpha值影响

        # 辅助变量,目的是提高算法执行效率
        self.sum_alpha = 0.0                        # 超参数alpha的和
        self.sum_beta = 0.0                         # 超参数beta的和
        self.sum_eta = [0.0 for i in range(self.M)]  # 超参数eta的和
        self.sum_gamma = [0.0 for i in range(self.M)]  # 超参数gamma的和
        self.sum_alpha_lambda = 0.0  # 超参数alpha_lambda的和

        # 先验知识,格式为{word_id: [k1, k2, ...], ...}
        self.prior_word = defaultdict(list)

        # 推断时需要的训练模型
        self.train_model = None
        return

    # --------------------------------------------------辅助函数---------------------------------------------------------
    def init_statistics_document(self):
        """
        :key: 初始化关于article的统计计数。先决条件: self.M, self.K, self.Z
        """
        assert self.M > 0 and self.K > 0 and self.Z

        # 统计计数初始化
        self.nd = numpy.zeros((self.M, self.K), dtype=numpy.int)
        self.ndsum = numpy.zeros((self.M, 1), dtype=numpy.int)
        self.ns = numpy.zeros((self.M, 4), dtype=numpy.int)
        self.nr = [numpy.zeros(len(i), dtype=numpy.int) for i in self.arts_ref]
        self.na = [numpy.zeros(len(i), dtype=numpy.int) for i in self.arts_auth]
        self.nssum = numpy.zeros((self.K, 1), dtype=numpy.int)
        self.an = numpy.zeros((len(self.authorids_list), self.K), dtype=numpy.int)
        self.ansum = numpy.zeros((len(self.authorids_list), 1), dtype=numpy.int)

        # 根据self.Z进行更新,更新self.nd[m, k]和self.ndsum[m, 0]
        for m in range(self.M):
            for k, s, r, a, c in zip(self.Z[m], self.S[m], self.R[m], self.A[m], self.C[m]):
                self.ns[m, s] += 1
                if s == 0:
                    self.nd[m, k] += 1
                    self.ndsum[m, 0] += 1
                elif s == 1:
                    self.nd[r, k] += 1
                    self.ndsum[r, 0] += 1
                    self.nr[m][r] += 1
                elif s == 2:
                    self.an[a, k] += 1
                    self.ansum[a, 0] += 1
                    self.na[m][a] += 1
                elif s == 3:
                    self.nd[c, k] += 1
                    self.ndsum[c, 0] += 1
            self.nssum[m, 0] = len(self.Z[m])
        return

    def init_statistics_word(self):
        """
        :key: 初始化关于word的统计计数。先决条件: self.V, self.K, self.Z, self.arts_Z
        """
        assert self.V > 0 and self.K > 0 and self.Z and self.arts_Z

        # 统计计数初始化
        self.nw = numpy.zeros((self.K, self.V), dtype=numpy.int)
        self.nwsum = numpy.zeros((self.K, 1), dtype=numpy.int)

        # 根据self.Z进行更新,更新self.nw[k, w]和self.nwsum[k, 0]
        for m in range(self.M):
            for k, w in zip(self.Z[m], self.arts_Z[m]):
                self.nw[k, w] += 1
                self.nwsum[k, 0] += 1
        return

    def init_statistics(self):
        """
        :key: 初始化全部的统计计数。上两个函数的综合函数。
        """
        self.init_statistics_document()
        self.init_statistics_word()
        return

    def sum_alpha_beta(self):
        """
        :key: 计算alpha、beta、eta、gamma、alpha_lambda的和
        """
        self.sum_alpha = self.alpha.sum()
        self.sum_beta = self.beta.sum()
        self.sum_eta = [i.sum() for i in self.eta]
        self.sum_gamma = [i.sum() for i in self.gamma]
        self.sum_alpha_lambda = self.alpha_lambda.sum()
        return

    def calculate_theta(self):
        """
        :key: 初始化并计算模型的theta值(M*K),用到alpha值
        """
        assert self.sum_alpha > 0
        self.theta = (self.nd + self.alpha) / (self.ndsum + self.sum_alpha)
        return

    def calculate_phi(self):
        """
        :key: 初始化并计算模型的phi值(K*V),用到beta值
        """
        assert self.sum_beta > 0
        self.phi = (self.nw + self.beta) / (self.nwsum + self.sum_beta)
        return

    def calculate_delta(self):
        """
        :key: 初始化并计算模型的delta值(M*Lm),用到eta值
        """
        # assert self.sum_alpha > 0
        self.delta = [(r + e) / (sr + se) for r, e, sr, se in zip(self.nr, self.eta, self.ns[:, 1], self.sum_eta)]
        return

    def calculate_mu(self):
        """
        :key: 初始化并计算模型的mu值(M*Am),用到gamma值
        """
        # assert self.sum_alpha > 0
        self.mu = [(a + g) / (sa + sg) for a, g, sa, sg in zip(self.na, self.gamma, self.ns[:, 2], self.sum_gamma)]
        return

    def calculate_llambda(self):
        """
        :key: 初始化并计算模型的lambda值(M*4),用到alpha_lambda值
        """
        assert self.sum_alpha_lambda > 0
        self.llambda = (self.ns + self.alpha_lambda) / (self.nssum + self.sum_alpha_lambda)
        return

    def calculate_theta_a(self):
        """
        :key: 初始化并计算模型的theta_a值(A*K),用到alpha值
        """
        assert self.sum_alpha > 0
        self.theta = (self.an + self.alpha) / (self.ansum + self.sum_alpha)
        return

    # ---------------------------------------------计算Perplexity值------------------------------------------------------
    def calculate_perplexity(self):
        """
        :key: 计算Perplexity值,并返回
        """
        # 计算theta.phi.delta.mu.llambda.theta_a值
        self.calculate_theta()
        self.calculate_phi()
        self.calculate_delta()
        self.calculate_mu()
        self.calculate_llambda()
        self.calculate_theta_a()

        # 开始计算
        preplexity = 0.0
        for m in range(self.M):
            for w in self.arts_Z[m]:
                p = self.llambda[m, 0] * numpy.sum(self.theta[m] * self.phi[:, w])
                p += self.llambda[m, 1] * numpy.sum(self.delta[m] * numpy.sum(self.theta[self.arts_ref[m]] * self.phi[:, w], 1))
                p += self.llambda[m, 2] * numpy.sum(self.mu[m] * numpy.sum(self.theta_a[self.arts_auth[m]] * self.phi[:, w], 1))
                p += self.llambda[m, 3] * numpy.sum(1.0 / (len(self.confs_paper[self.artconfs_list[m]]) - 1) * numpy.array(
                    [numpy.sum(self.theta[conf] * self.phi[:, w]) for conf in
                     self.confs_paper[self.artconfs_list[m]] if conf != m]))
                preplexity += numpy.log(p)
        return numpy.exp(-(preplexity / self.words_count))

    # --------------------------------------------------静态函数---------------------------------------------------------
    @staticmethod
    def multinomial_sample(pro_list):
        """
        :key: 静态函数,多项式分布抽样,此时会改变pro_list的值
        :param pro_list: [0.2, 0.7, 0.4, 0.1],此时说明返回下标1的可能性大,但也不绝对
        """
        # 将pro_list进行累加
        for k in range(1, len(pro_list)):
            pro_list[k] += pro_list[k-1]

        # 确定随机数 u 落在哪个下标值,此时的下标值即为抽取的类别（random.rand()返回: [0, 1.0)）
        u = numpy.random.rand() * pro_list[-1]

        return_index = len(pro_list) - 1
        for t in range(len(pro_list)):
            if pro_list[t] > u:
                return_index = t
                break
        return return_index

    # ----------------------------------------------Gibbs抽样算法--------------------------------------------------------
    def gibbs_sampling(self, is_calculate_preplexity):
        """
        :key: LDA模型中的Gibbs抽样过程
        :param is_calculate_preplexity: 是否计算preplexity值
        """
        # 计算preplexity值用到的变量
        pp_list = []
        pp_var = numpy.inf

        # 开始迭代
        last_iter = self.current_iter + 1
        iters_num = self.iters_num if self.iters_num != "auto" else MAX_ITER_NUM
        for self.current_iter in range(last_iter, last_iter+iters_num):
            info = "......"

            # 是否计算preplexity值
            if is_calculate_preplexity:
                pp = self.calculate_perplexity()
                pp_list.append(pp)

                # 计算列表最新VAR_NUM项的方差
                pp_var = numpy.var(pp_list[-VAR_NUM:]) if len(pp_list) >= VAR_NUM else numpy.inf
                info = (", preplexity: " + str(pp)) + ((", var: " + str(pp_var)) if len(pp_list) >= VAR_NUM else "")

            # 输出Debug信息
            logging.debug("\titeration " + str(self.current_iter) + info)

            # 判断是否跳出循环
            if self.iters_num == "auto" and pp_var < (VAR_NUM / 2):
                break

            # 对每篇article的每个word进行一次抽样,抽取合适的k值
            for m in range(self.M):
                for n in range(len(self.Z[m])):
                    w = self.arts_Z[m][n]
                    k = self.Z[m][n]
                    s = self.S[m][n]
                    r = self.R[m][n]
                    a = self.A[m][n]
                    c = self.C[m][n]

                    # 统计计数减一
                    self.nw[k, w] -= 1
                    self.nwsum[k, 0] -= 1
                    self.ns[m, s] -= 1
                    self.nssum[m, 0] -= 1
                    if s == 0:
                        self.nd[m, k] -= 1
                        self.ndsum[m, 0] -= 1
                    elif s == 1:
                        self.nd[r, k] -= 1
                        self.ndsum[r, 0] -= 1
                        self.nr[m][r] -= 1
                    elif s == 2:
                        self.an[a, k] -= 1
                        self.ansum[a, 0] -= 1
                        self.na[m][a] -= 1
                    elif s == 3:
                        self.nd[c, k] -= 1
                        self.ndsum[c, 0] -= 1

                    # if self.prior_word and (w in self.prior_word):
                    #     # 带有先验知识,否则进行正常抽样
                    #     k = numpy.random.choice(self.prior_word[w])
                    # else:
                    #     # 计算theta值--下边的过程为抽取第m篇article的第n个词w的topic,即新的k
                    #     theta_p = (self.nd[m] + self.alpha) / (self.ndsum[m, 0] + self.sum_alpha)
                    #
                    #     # 计算phi值--判断是训练模型,还是推断模型（注意self.beta[w_g]）
                    #     if self.local_2_global and self.train_model:
                    #         w_g = self.local_2_global[w]
                    #         phi_p = (self.train_model.nw[:, w_g] + self.nw[:, w] + self.beta[w_g]) / \
                    #                 (self.train_model.nwsum[:, 0] + self.nwsum[:, 0] + self.sum_beta)
                    #     else:
                    #         phi_p = (self.nw[:, w] + self.beta[w]) / (self.nwsum[:, 0] + self.sum_beta)
                    #
                    #     # multi_p为多项式分布的参数,此时没有进行标准化
                    #     multi_p = theta_p * phi_p
                    #
                    #     # 此时的topic即为Gibbs抽样得到的topic,它有较大的概率命中多项式概率大的topic
                    #     k = LdaBase.multinomial_sample(multi_p)

                    # 计算llambda值--下边的过程为抽取第m篇article的第n个词w的source,即新的s
                    llambda_p = (self.ns[m] + self.alpha_lambda) / (self.nssum[m] + self.sum_alpha_lambda)
                    # 计算theta值
                    theta_p0 = (self.nd[m, k] + self.alpha[k]) / (self.ndsum[m, 0] + self.sum_alpha)
                    theta_p1 = (self.nd[r, k] + self.alpha[k]) / (self.ndsum[r, 0] + self.sum_alpha)
                    theta_p2 = (self.an[a, k] + self.alpha[k]) / (self.ansum[a, 0] + self.sum_alpha)
                    theta_p3 = (self.nd[c, k] + self.alpha[k]) / (self.ndsum[c, 0] + self.sum_alpha)
                    theta_p = numpy.array([theta_p0, theta_p1, theta_p2, theta_p3])
                    # multi_p为多项式分布的参数,此时没有进行标准化
                    multi_p = theta_p * llambda_p
                    # 此时的source即为Gibbs抽样得到的source,它有较大的概率命中多项式概率大的source
                    s = LdaBase.multinomial_sample(multi_p)

                    if s == 0:
                        # 计算theta值--下边的过程为抽取第m篇article的第n个词w的topic,即新的k
                        theta_p = (self.nd[m] + self.alpha) / (self.ndsum[m, 0] + self.sum_alpha)
                        # 计算phi值
                        phi_p = (self.nw[:, w] + self.beta[w]) / (self.nwsum[:, 0] + self.sum_beta)
                        # multi_p为多项式分布的参数,此时没有进行标准化
                        multi_p = theta_p * phi_p
                        # 此时的topic即为Gibbs抽样得到的topic,它有较大的概率命中多项式概率大的topic
                        k = LdaBase.multinomial_sample(multi_p)
                        # 统计计数加一
                        self.nd[m, k] += 1
                        self.ndsum[m, 0] += 1
                    elif s == 1:
                        # 计算theta值--下边的过程为抽取第m篇article的第n个词w的ref,即新的r
                        theta_p = numpy.array(
                            [(self.nd[ref, k] + self.alpha[k]) / (self.ndsum[ref, 0] + self.sum_alpha) for ref in
                             self.arts_ref[m]])
                        # 计算delta值
                        delta_p = (self.nr[m] + self.eta[m]) / (self.ns[m, s] + self.sum_eta[m])
                        # multi_p为多项式分布的参数,此时没有进行标准化
                        multi_p = theta_p * delta_p
                        # 此时的ref即为Gibbs抽样得到的ref,它有较大的概率命中多项式概率大的ref
                        r = LdaBase.multinomial_sample(multi_p)

                        # 计算theta值--下边的过程为抽取第m篇article的第n个词w的topic,即新的k
                        theta_p = (self.nd[r] + self.alpha) / (self.ndsum[r, 0] + self.sum_alpha)
                        # 计算phi值
                        phi_p = (self.nw[:, w] + self.beta[w]) / (self.nwsum[:, 0] + self.sum_beta)
                        # multi_p为多项式分布的参数,此时没有进行标准化
                        multi_p = theta_p * phi_p
                        # 此时的topic即为Gibbs抽样得到的topic,它有较大的概率命中多项式概率大的topic
                        k = LdaBase.multinomial_sample(multi_p)
                        # 统计计数加一
                        self.nd[r, k] += 1
                        self.ndsum[r, 0] += 1
                        self.nr[m][r] += 1
                    elif s == 2:
                        # 计算theta_a值--下边的过程为抽取第m篇article的第n个词w的author,即新的a
                        theta_a_p = numpy.array(
                            [(self.an[auth, k] + self.alpha[k]) / (self.ansum[auth, 0] + self.sum_alpha) for auth in
                             self.arts_auth[m]])
                        # 计算mu值
                        mu_p = (self.na[m] + self.gamma[m]) / (self.ns[m, s] + self.sum_gamma[m])
                        # multi_p为多项式分布的参数,此时没有进行标准化
                        multi_p = theta_a_p * mu_p
                        # 此时的author即为Gibbs抽样得到的author,它有较大的概率命中多项式概率大的author
                        a = LdaBase.multinomial_sample(multi_p)

                        # 计算theta值--下边的过程为抽取第m篇article的第n个词w的topic,即新的k
                        theta_p = (self.an[a] + self.alpha) / (self.ansum[a, 0] + self.sum_alpha)
                        # 计算phi值
                        phi_p = (self.nw[:, w] + self.beta[w]) / (self.nwsum[:, 0] + self.sum_beta)
                        # multi_p为多项式分布的参数,此时没有进行标准化
                        multi_p = theta_p * phi_p
                        # 此时的topic即为Gibbs抽样得到的topic,它有较大的概率命中多项式概率大的topic
                        k = LdaBase.multinomial_sample(multi_p)
                        # 统计计数加一
                        self.an[a, k] += 1
                        self.ansum[a, 0] += 1
                        self.na[m][a] += 1
                    elif s == 3:
                        # 计算theta值--下边的过程为抽取第m篇article的第n个词w的paper-conf,即新的c
                        theta_p = numpy.array(
                            [(self.nd[conf, k] + self.alpha[k]) / (self.ndsum[conf, 0] + self.sum_alpha) for conf in
                             self.confs_paper[self.artconfs_list[m]] if conf != m])
                        # 计算Q值
                        q_p = numpy.ones(len(self.confs_paper[self.artconfs_list[m]]) - 1) / (len(self.confs_paper[self.artconfs_list[m]]) - 1)
                        # multi_p为多项式分布的参数,此时没有进行标准化
                        multi_p = theta_p * q_p
                        # 此时的paper-conf即为Gibbs抽样得到的paper-conf,它有较大的概率命中多项式概率大的paper-conf
                        c = LdaBase.multinomial_sample(multi_p)

                        # 计算theta值--下边的过程为抽取第m篇article的第n个词w的topic,即新的k
                        theta_p = (self.nd[c] + self.alpha) / (self.ndsum[c, 0] + self.sum_alpha)
                        # 计算phi值
                        phi_p = (self.nw[:, w] + self.beta[w]) / (self.nwsum[:, 0] + self.sum_beta)
                        # multi_p为多项式分布的参数,此时没有进行标准化
                        multi_p = theta_p * phi_p
                        # 此时的topic即为Gibbs抽样得到的topic,它有较大的概率命中多项式概率大的topic
                        k = LdaBase.multinomial_sample(multi_p)
                        # 统计计数加一
                        self.nd[c, k] += 1
                        self.ndsum[c, 0] += 1

                    # 统计计数加一
                    self.nw[k, w] += 1
                    self.nwsum[k, 0] += 1
                    self.ns[m, s] += 1
                    self.nssum[m, 0] += 1

                    # 更新ZSRAC值
                    self.Z[m][n] = k
                    self.S[m][n] = s
                    self.R[m][n] = r
                    self.A[m][n] = a
                    self.C[m][n] = c
        # 抽样完毕
        return

    # -----------------------------------------Model数据存储、读取相关函数-------------------------------------------------
    def save_parameter(self, file_name):
        """
        :key: 保存模型相关参数数据,包括: topics_num, M, V, K, words_count, alpha, beta, eta, gamma, alpha_lambda
        """
        with open(file_name, "w", encoding="utf-8") as f_param:
            for item in ["topics_num", "M", "V", "K", "words_count"]:
                f_param.write("%s\t%s\n" % (item, str(self.__dict__[item])))
            f_param.write("alpha\t%s\n" % ",".join([str(item) for item in self.alpha]))
            f_param.write("beta\t%s\n" % ",".join([str(item) for item in self.beta]))
            for line in self.eta:
                f_param.write("eta\t%s\n" % ",".join([str(item) for item in line]))
            for line in self.gamma:
                f_param.write("gamma\t%s\n" % ",".join([str(item) for item in line]))
            f_param.write("alpha_lambda\t%s\n" % ",".join([str(item) for item in self.alpha_lambda]))
        return

    def load_parameter(self, file_name):
        """
        :key: 加载模型相关参数数据,和上一个函数相对应
        """
        with open(file_name, "r", encoding="utf-8") as f_param:
            for line in f_param:
                key, value = line.strip().split()
                if key in ["topics_num", "M", "V", "K", "words_count"]:
                    self.__dict__[key] = int(value)
                elif key in ["alpha", "beta"]:
                    self.__dict__[key] = numpy.array([float(item) for item in value.split(",")])
        return

    def save_zvalue(self, file_name):
        """
        :key: 保存模型关于article的变量,包括: arts_Z, Z, S, R, A, C, artids_list, arts_ref, arts_auth, artconfs_list等
        """
        with open(file_name, "w", encoding="utf-8") as f_zvalue:
            for m in range(self.M):
                out_line = [str(w) + ":" + str(k) + ":" + str(s) + ":" + str(r) + ":" + str(a) + ":" + str(c)
                            for w, k, s, r, a, c in
                            zip(self.arts_Z[m], self.Z[m], self.S[m], self.R[m], self.A[m], self.C[m])]
                f_zvalue.write("words\t" + self.artids_list[m] + "\t" + " ".join(out_line) + "\n")
                f_zvalue.write("arts_ref\t" + self.artids_list[m] + "\t" + " ".join([str(item) for item in self.arts_ref[m]]) + "\n")
                f_zvalue.write("arts_auth\t" + self.artids_list[m] + "\t" + " ".join([str(item) for item in self.arts_auth[m]]) + "\n")
            f_zvalue.write("artconfs_list\t%s\n" % " ".join([str(item) for item in self.artconfs_list]))
        return

    def load_zvalue(self, file_name):
        """
        :key: 读取模型的Z变量。和上一个函数相对应
        """
        self.arts_Z = []
        self.artids_list = []
        self.Z = []
        with open(file_name, "r", encoding="utf-8") as f_zvalue:
            for line in f_zvalue:
                frags = line.strip().split()
                art_id = frags[0].strip()
                w_k_list = [value.split(":") for value in frags[1:]]
                # 添加到类中
                self.artids_list.append(art_id)
                self.arts_Z.append([int(item[0]) for item in w_k_list])
                self.Z.append([int(item[1]) for item in w_k_list])
        return

    def save_author(self, file_name):
        """
        :key: 保存模型关于author的变量,包括: authorids_list, auths_paper
        """
        with open(file_name, "w", encoding="utf-8") as f_author:
            for a in range(len(self.authorids_list)):
                f_author.write(self.authorids_list[a] + "\t" + ",".join([str(item) for item in self.auths_paper[a]]) + "\n")
        return

    def save_conf(self, file_name):
        """
        :key: 保存模型关于conf的变量,包括: confids_list, confs_paper
        """
        with open(file_name, "w", encoding="utf-8") as f_conf:
            for c in range(len(self.confids_list)):
                f_conf.write(self.confids_list[c] + "\t" + ",".join([str(item) for item in self.confs_paper[c]]) + "\n")
        return

    def save_twords(self, file_name):
        """
        :key: 保存模型的twords数据,要用到phi的数据
        """
        self.calculate_phi()
        out_num = self.V if self.twords_num > self.V else self.twords_num
        with open(file_name, "w", encoding="utf-8") as f_twords:
            for k in range(self.K):
                words_list = sorted([(w, self.phi[k, w]) for w in range(self.V)], key=lambda x: x[1], reverse=True)
                f_twords.write("Topic %dth:\n" % k)
                f_twords.writelines(["\t%s %f\n" % (self.local_bi.get_value(w), p) for w, p in words_list[:out_num]])
        return

    def load_twords(self, file_name):
        """
        :key: 加载模型的twords数据,即先验数据
        """
        self.prior_word.clear()
        topic = -1
        with open(file_name, "r", encoding="utf-8") as f_twords:
            for line in f_twords:
                if line.startswith("Topic"):
                    topic = int(line.strip()[6:-3])
                else:
                    word_id = self.local_bi.get_key(line.strip().split()[0].strip())
                    self.prior_word[word_id].append(topic)
        return

    def save_tag(self, file_name):
        """
        :key: 输出模型最终给数据打标签的结果,用到theta值
        """
        self.calculate_theta()
        with open(file_name, "w", encoding="utf-8") as f_tag:
            for m in range(self.M):
                f_tag.write("%s\t%s\n" % (self.artids_list[m], " ".join([str(item) for item in self.theta[m]])))
        return

    def save_delta(self, file_name):
        """
        :key: 输出模型最终给数据打标签的结果,用到phi值
        """
        self.calculate_delta()
        with open(file_name, "w", encoding="utf-8") as f_delta:
            for m in range(self.M):
                f_delta.write("%s\t%s\n" % (self.artids_list[m], " ".join([str(item) for item in self.delta[m]])))
        return

    def save_mu(self, file_name):
        """
        :key: 输出模型最终给数据打标签的结果,用到mu值
        """
        self.calculate_mu()
        with open(file_name, "w", encoding="utf-8") as f_mu:
            for m in range(self.M):
                f_mu.write("%s\t%s\n" % (self.artids_list[m], " ".join([str(item) for item in self.mu[m]])))
        return

    def save_llambda(self, file_name):
        """
        :key: 输出模型最终给数据打标签的结果,用到theta值
        """
        self.calculate_llambda()
        with open(file_name, "w", encoding="utf-8") as f_llambda:
            for m in range(self.M):
                f_llambda.write("%s\t%s\n" % (self.artids_list[m], " ".join([str(item) for item in self.llambda[m]])))
        return

    def save_tag_a(self, file_name):
        """
        :key: 输出模型最终给数据打标签的结果,用到theta_a值
        """
        self.calculate_theta_a()
        with open(file_name, "w", encoding="utf-8") as f_tag_a:
            for a in range(len(self.authorids_list)):
                f_tag_a.write("%s\t%s\n" % (self.authorids_list[a], " ".join([str(item) for item in self.theta_a[a]])))
        return

    def save_model(self):
        """
        :key: 保存模型数据
        """
        name_predix = "%s-%05d" % (self.model_name, self.current_iter)

        # 保存训练结果
        self.save_parameter(os.path.join(self.dir_path, "%s.%s" % (name_predix, "param")))
        self.save_wordmap(os.path.join(self.dir_path, "%s.%s" % (name_predix, "wordmap")))
        self.save_zvalue(os.path.join(self.dir_path, "%s.%s" % (name_predix, "zvalue")))
        self.save_author(os.path.join(self.dir_path, "%s.%s" % (name_predix, "author")))
        self.save_conf(os.path.join(self.dir_path, "%s.%s" % (name_predix, "conf")))

        #保存额外数据
        self.save_twords(os.path.join(self.dir_path, "%s.%s" % (name_predix, "twords")))
        self.save_tag(os.path.join(self.dir_path, "%s.%s" % (name_predix, "tag")))
        self.save_delta(os.path.join(self.dir_path, "%s.%s" % (name_predix, "delta")))
        self.save_mu(os.path.join(self.dir_path, "%s.%s" % (name_predix, "mu")))
        self.save_llambda(os.path.join(self.dir_path, "%s.%s" % (name_predix, "llambda")))
        self.save_tag_a(os.path.join(self.dir_path, "%s.%s" % (name_predix, "tag_a")))
        return

    def load_model(self):
        """
        :key: 加载模型数据
        """
        name_predix = "%s-%05d" % (self.model_name, self.current_iter)

        # 加载训练结果
        self.load_parameter(os.path.join(self.dir_path, "%s.%s" % (name_predix, "param")))
        self.load_wordmap(os.path.join(self.dir_path, "%s.%s" % (name_predix, "wordmap")))
        self.load_zvalue(os.path.join(self.dir_path, "%s.%s" % (name_predix, "zvalue")))
        return


class LdaModel(LdaBase):
    """
    LDA模型定义,主要实现训练、继续训练、推断的过程
    """

    def init_train_model(self, ip, port, dir_path, model_name, current_iter, iters_num=None, topics_num=20, twords_num=200,
                         alpha=-1.0, beta=0.01, eta=-1.0, gamma=-1.0, alpha_lambda=-1.0, data_file="", prior_file=""):
        """
        :key: 初始化训练模型,根据参数current_iter（是否等于0）决定是初始化新模型,还是加载已有模型
        :key: 当初始化新模型时,除了prior_file先验文件外,其余所有的参数都需要,且current_iter等于0
        :key: 当加载已有模型时,只需要dir_path, model_name, current_iter（不等于0）, iters_num, twords_num即可
        :param iters_num: 可以为整数值或者“auto”
        """
        if current_iter == 0:
            logging.debug("init a new train model")

            # 初始化语料集
            # self.init_corpus_with_file(data_file)
            self.init_corpus_with_mongodb(ip, port)

            # 初始化部分变量
            self.dir_path = dir_path
            self.model_name = model_name
            self.current_iter = current_iter
            self.iters_num = iters_num
            self.topics_num = topics_num
            self.K = topics_num
            self.twords_num = twords_num

            # 初始化alpha和beta
            self.alpha = numpy.array([alpha if alpha > 0 else (50.0/self.K) for k in range(self.K)])
            self.beta = numpy.array([beta if beta > 0 else 0.01 for w in range(self.V)])
            self.eta = [numpy.array([eta if eta > 0 else (50.0/len(m)) for i in m]) for m in self.arts_ref]
            self.gamma = [numpy.array([gamma if gamma > 0 else (50.0/len(a)) for i in a]) for a in self.arts_auth]
            self.alpha_lambda = numpy.ones(4) * (alpha_lambda if alpha_lambda > 0 else 12.5)

            # 初始化Z值,以便统计计数
            self.Z = [[numpy.random.randint(self.K) for n in range(len(self.arts_Z[m]))] for m in range(self.M)]
            self.S = [[numpy.random.randint(4) for n in range(len(self.arts_Z[m]))] for m in range(self.M)]
            self.R = [[numpy.random.randint(len(self.arts_ref[m])) for n in range(len(self.arts_Z[m]))] for m in range(self.M)]
            self.A = [[numpy.random.randint(len(self.arts_auth[m])) for n in range(len(self.arts_Z[m]))] for m in range(self.M)]
            self.C = [[numpy.random.randint(len(self.confs_paper[self.artconfs_list[m]])-1) for n in range(len(self.arts_Z[m]))] for m in range(self.M)]
        else:
            logging.debug("init an existed model")

            # 初始化部分变量
            self.dir_path = dir_path
            self.model_name = model_name
            self.current_iter = current_iter
            self.iters_num = iters_num
            self.twords_num = twords_num

            # 加载已有模型
            self.load_model()

        # 初始化统计计数
        self.init_statistics()

        # 计算alpha和beta的和值
        self.sum_alpha_beta()

        # 初始化先验知识
        if prior_file:
            self.load_twords(prior_file)

        # 返回该模型
        return self

    def begin_gibbs_sampling_train(self, is_calculate_preplexity=True):
        """
        :key: 训练模型,对语料集中的所有数据进行Gibbs抽样,并保存最后的抽样结果
        """
        # Gibbs抽样
        logging.debug("sample iteration start, iters_num: " + str(self.iters_num))
        self.gibbs_sampling(is_calculate_preplexity)
        logging.debug("sample iteration finish")

        # 保存模型
        logging.debug("save model")
        self.save_model()
        return

    def init_inference_model(self, train_model):
        """
        :key: 初始化推断模型
        """
        self.train_model = train_model

        # 初始化变量: 主要用到self.topics_num, self.K
        self.topics_num = train_model.topics_num
        self.K = train_model.K

        # 初始化变量self.alpha, self.beta,直接沿用train_model的值
        self.alpha = train_model.alpha      # K维的float值,训练和推断模型中的K相同,故可以沿用
        self.beta = train_model.beta        # V维的float值,推断模型中用于计算phi的V值应该是全局的word的数量,故可以沿用
        self.sum_alpha_beta()               # 计算alpha和beta的和

        # 初始化数据集的self.global_bi
        self.global_bi = train_model.local_bi
        return

    def inference_data(self, article_list, iters_num=100, repeat_num=3):
        """
        :key: 利用现有模型推断数据
        :param article_list: 每一行的数据格式为: id[tab]word1 word2 word3......
        :param iters_num: 每一次迭代的次数
        :param repeat_num: 重复迭代的次数
        """
        # 初始化语料集
        self.init_corpus_with_articles(article_list)

        # 初始化返回变量
        return_theta = numpy.zeros((self.M, self.K))

        # 重复抽样
        for i in range(repeat_num):
            logging.debug("inference repeat_num: " + str(i+1))

            # 初始化变量
            self.current_iter = 0
            self.iters_num = iters_num

            # 初始化Z值,以便统计计数
            self.Z = [[numpy.random.randint(self.K) for n in range(len(self.arts_Z[m]))] for m in range(self.M)]

            # 初始化统计计数
            self.init_statistics()

            # 开始推断
            self.gibbs_sampling(is_calculate_preplexity=False)

            # 计算theta
            self.calculate_theta()
            return_theta += self.theta

        # 计算结果,并返回
        return return_theta / repeat_num


if __name__ == "__main__":
    """
    测试代码
    """
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s\t%(levelname)s\t%(message)s")

    # train或者inference
    test_type = "train"
    # test_type = "inference"

    # 测试新模型
    if test_type == "train":
        model = LdaModel()
        # 由prior_file决定是否带有先验知识
        model.init_train_model("localhost", 17012, "data/", "model", current_iter=0, iters_num="auto", topics_num=20)
        # model.init_train_model("data/", "model", current_iter=0, iters_num="auto", topics_num=10, data_file="corpus.txt", prior_file="prior.twords")
        model.begin_gibbs_sampling_train()
    elif test_type == "inference":
        model = LdaModel()
        model.init_inference_model(LdaModel().init_train_model("data/", "model", current_iter=134))
        data = [
            "cn	咪咕 漫画 咪咕 漫画 漫画 更名 咪咕 漫画 资源 偷星 国漫 全彩 日漫 实时 在线看 随心所欲 登陆 漫画 资源 黑白 全彩 航海王",
            "co	aircloud aircloud 硬件 设备 wifi 智能 手要 平板电脑 电脑 存储 aircloud 文件 远程 型号 aircloud 硬件 设备 wifi"
        ]
        result = model.inference_data(data)

    # 退出程序
    exit()
