# pointcnn_vkitti3d_tool
training and testing vkitti3d dataset using pointcnn

有关pointcnn的一个小工作，主要是验证工具和一些写的小玩意，训练代码估计是没得放出了。毕竟不是自己写的（笑

eval是来自于pointcnn主仓库里的eval_s3dis代码，作者写了semantic3d的训练和合并但是不知道为什么没写eval。我模型是照着pointcnn里semantic3d写的，要评价干脆自己写了一个，加上了mAcc.

calculate是拿来搞交叉验证的，原来的代码每换一个区域就要更新一次merge里的字典实在是太烦，干脆全改了让程序自己生成字典，这个算是实验的小东西

prediction是拿来转pcd用来做可视化的，会转出源文件，标签和预测三个pcd来，后面的事情就是pcl要做得了，那个代码传不传就随缘了
