from __future__ import absolute_import

import torch
from torch import nn
from torch.nn import functional as F
import torchvision

__all__ = ['DenseNet121', 'DenseNet121_salience', 'DenseNet121_parsing', 'DenseNet121_full']

class DenseNet121(nn.Module):
    """
    Code imported from https://github.com/KaiyangZhou/deep-person-reid
    """
    def __init__(self, num_classes, loss={'xent'}, **kwargs):
        super(DenseNet121, self).__init__()
        self.loss = loss
        densenet121 = torchvision.models.densenet121(pretrained=True)
        self.base = densenet121.features
        self.classifier = nn.Linear(1024, num_classes)
        self.feat_dim = 1024 # feature dimension
        self.use_salience = False
        self.use_parsing = False

    def forward(self, x):
        x = self.base(x)
        x = F.avg_pool2d(x, x.size()[2:])
        f = x.view(x.size(0), -1)
        if not self.training:
            return f
        y = self.classifier(f)
        
        if self.loss == {'xent'}:
            return y
        elif self.loss == {'xent', 'htri'}:
            return y, f
        elif self.loss == {'cent'}:
            return y, f
        elif self.loss == {'ring'}:
            return y, f
        else:
            raise KeyError("Unsupported loss: {}".format(self.loss))

class DenseNet121_salience_beg(nn.Module):
    ' deprecated '
    def __init__(self, num_classes, loss={'xent'}, **kwargs):
        super(DenseNet121_salience_beg, self).__init__()
        self.loss = loss
        densenet121 = torchvision.models.densenet121(pretrained=True)
        self.base0 = densenet121.features[0]
        self.base1 = densenet121.features[1]
        self.base2 = densenet121.features[2]
        self.base3 = densenet121.features[3]
        self.base4 = densenet121.features[4]#dense block
        self.base5 = densenet121.features[5]#composite function
        self.base6 = densenet121.features[6]#dense block
        self.base7 = densenet121.features[7]#composite function
        self.base8 = densenet121.features[8]#dense block
        self.base9 = densenet121.features[9]#composite function
        self.base10 = densenet121.features[10]#dense block
        self.base11 = densenet121.features[11]#batch normalization
        
        self.classifier = nn.Linear(1024, num_classes)
        self.feat_dim = 1024 # feature dimension
        self.use_salience = True
        self.use_parsing = False

    def forward(self, x, salience_masks):
        salience_masks = salience_masks.view(salience_masks.size(0), 1, salience_masks.size(1), salience_masks.size(2))
        salience_masks = F.upsample(salience_masks, size = (parsing_masks.size()[-2], parsing_masks.size()[-1]), mode = 'bilinear')

        x = x * salience_masks
        x = self.base0(x)
        x = self.base1(x)
        x = self.base2(x)
        x = self.base3(x)
        x = self.base4(x)
        x = self.base5(x)
        x = self.base6(x)
        x = self.base7(x)
        x = self.base8(x)
        x = self.base9(x)
        x = self.base10(x)
        x = self.base11(x)

        x = F.avg_pool2d(x, x.size()[2:])

        f = x.view(x.size(0), -1)
        if not self.training:
            return f
        y = self.classifier(f)
        
        if self.loss == {'xent'}:
            return y
        elif self.loss == {'xent', 'htri'}:
            return y, f
        elif self.loss == {'cent'}:
            return y, f
        elif self.loss == {'ring'}:
            return y, f
        else:
            raise KeyError("Unsupported loss: {}".format(self.loss))

class DenseNet121_parsing_beg(nn.Module):
    ' deprecated '    
    def __init__(self, num_classes, loss={'xent'}, **kwargs):
        super(DenseNet121_parsing_beg, self).__init__()
        self.loss = loss
        densenet121 = torchvision.models.densenet121(pretrained=True)
        self.base0 = densenet121.features[0]
        self.base1 = densenet121.features[1]
        self.base2 = densenet121.features[2]
        self.base3 = densenet121.features[3]
        self.base4 = densenet121.features[4]#dense block
        self.base5 = densenet121.features[5]#composite function
        self.base6 = densenet121.features[6]#dense block
        self.base7 = densenet121.features[7]#composite function
        self.base8 = densenet121.features[8]#dense block
        self.base9 = densenet121.features[9]#composite function
        self.base10 = densenet121.features[10]#dense block
        self.base11 = densenet121.features[11]#batch normalization
        
        self.classifier = nn.Linear(1024, num_classes)
        self.feat_dim = 1024 # feature dimension
        self.use_salience = False
        self.use_parsing = True

    def forward(self, x, parsing_masks):
        parsing_masks = parsing_masks[:, 0] #recover just foreground
        parsing_masks = parsing_masks.view(parsing_masks.size(0), 1, parsing_masks.size(1), parsing_masks.size(2))
        parsing_masks = F.upsample(parsing_masks, size = (parsing_masks.size()[-2], parsing_masks.size()[-1]), mode = 'bilinear')

        x = x * parsing_masks
        x = self.base0(x)
        x = self.base1(x)
        x = self.base2(x)
        x = self.base3(x)
        x = self.base4(x)
        x = self.base5(x)
        x = self.base6(x)
        x = self.base7(x)
        x = self.base8(x)
        x = self.base9(x)
        x = self.base10(x)
        x = self.base11(x)

        x = F.avg_pool2d(x, x.size()[2:])

        f = x.view(x.size(0), -1)
        if not self.training:
            return f
        y = self.classifier(f)
        
        if self.loss == {'xent'}:
            return y
        elif self.loss == {'xent', 'htri'}:
            return y, f
        elif self.loss == {'cent'}:
            return y, f
        elif self.loss == {'ring'}:
            return y, f
        else:
            raise KeyError("Unsupported loss: {}".format(self.loss))

class DenseNet121_salience(nn.Module):
    def __init__(self, num_classes, loss={'xent'}, **kwargs):
        super(DenseNet121_salience, self).__init__()
        self.loss = loss
        densenet121 = torchvision.models.densenet121(pretrained=True)
        self.base0 = densenet121.features[0]
        self.base1 = densenet121.features[1]
        self.base2 = densenet121.features[2]
        self.base3 = densenet121.features[3]
        self.base4 = densenet121.features[4]#dense block
        self.base5 = densenet121.features[5]#composite function
        self.base6 = densenet121.features[6]#dense block
        self.base7 = densenet121.features[7]#composite function
        self.base8 = densenet121.features[8]#dense block
        self.base9 = densenet121.features[9]#composite function
        self.base10 = densenet121.features[10]#dense block
        self.base11 = densenet121.features[11]#batch normalization
        
        self.classifier = nn.Linear(1280, num_classes)
        self.feat_dim = 1280 # feature dimension
        self.use_salience = True
        self.use_parsing = False

    def forward(self, x, salience_masks):

        x = self.base0(x)
        x = self.base1(x)
        x = self.base2(x)
        x = self.base3(x)
        x = self.base4(x)
        x = self.base5(x)
        x = self.base6(x)
        x7= self.base7(x)#size = 256, 16, 8
        x = self.base8(x7)
        x = self.base9(x)
        x = self.base10(x)
        x = self.base11(x)

        x = F.avg_pool2d(x, x.size()[2:])
        x = x.view(x.size(0), -1)
        
        #upsample feature map to fit salience_masks
        salience_feat = F.upsample(x7, size = (salience_masks.size()[-2], salience_masks.size()[-1]), mode = 'bilinear')
        #combine feature map with salience_masks (128, 64)
        channel_size = salience_feat.size()[2] * salience_feat.size()[3]
        salience_masks = salience_masks.cuda()
        salience_masks = salience_masks.view(salience_masks.size()[0], channel_size, 1)
        salience_feat = salience_feat.view(salience_feat.size()[0], salience_feat.size()[1], channel_size)
        salience_feat  = torch.bmm(salience_feat, salience_masks)#instead of replicating we use matrix product
        #average pooling
        salience_feat = salience_feat.view(salience_feat.size()[:2]) / float(channel_size)

        f = torch.cat((x, salience_feat), dim = 1)

        if not self.training:
            return f
        y = self.classifier(f)
        
        if self.loss == {'xent'}:
            return y
        elif self.loss == {'xent', 'htri'}:
            return y, f
        elif self.loss == {'cent'}:
            return y, f
        elif self.loss == {'ring'}:
            return y, f
        else:
            raise KeyError("Unsupported loss: {}".format(self.loss))

class DenseNet121_parsing(nn.Module):
    def __init__(self, num_classes, loss={'xent'}, **kwargs):
        super(DenseNet121_parsing, self).__init__()
        self.loss = loss
        densenet121 = torchvision.models.densenet121(pretrained=True)
        self.base0 = densenet121.features[0]
        self.base1 = densenet121.features[1]
        self.base2 = densenet121.features[2]
        self.base3 = densenet121.features[3]
        self.base4 = densenet121.features[4]#dense block
        self.base5 = densenet121.features[5]#composite function
        self.base6 = densenet121.features[6]#dense block
        self.base7 = densenet121.features[7]#composite function
        self.base8 = densenet121.features[8]#dense block
        self.base9 = densenet121.features[9]#composite function
        self.base10 = densenet121.features[10]#dense block
        self.base11 = densenet121.features[11]#batch normalization
        
        self.classifier = nn.Linear(2304, num_classes)
        self.feat_dim = 2304 # feature dimension
        self.use_salience = False
        self.use_parsing = True

    def forward(self, x, parsing_masks):

        x = self.base0(x)
        x = self.base1(x)
        x = self.base2(x)
        x = self.base3(x)
        x = self.base4(x)
        x = self.base5(x)
        x = self.base6(x)
        x7= self.base7(x)#size = 256, 16, 8
        x = self.base8(x7)
        x = self.base9(x)
        x = self.base10(x)
        x = self.base11(x)

        x = F.avg_pool2d(x, x.size()[2:])
        x = x.view(x.size(0), -1)
        
        #upsample feature map to fit salience_masks
        parsing_feat = F.upsample(x7, size = (parsing_masks.size()[-2], parsing_masks.size()[-1]), mode = 'bilinear')
        #combine feature map with salience_masks (128, 64)
        channel_size = parsing_feat.size()[2] * parsing_feat.size()[3]
        parsing_masks = parsing_masks.view(parsing_masks.size()[0], parsing_masks.size()[1], channel_size)
        parsing_masks = torch.transpose(parsing_masks, 1, 2)
        parsing_feat = parsing_feat.view(parsing_feat.size()[0], parsing_feat.size()[1], channel_size)
        parsing_feat = torch.bmm(parsing_feat, parsing_masks)
        #average pooling
        parsing_feat = parsing_feat.view(parsing_feat.size()[0], parsing_feat.size()[1] * parsing_feat.size()[2]).cuda() / float(channel_size)

        f = torch.cat((x, parsing_feat), dim = 1)

        if not self.training:
            return f
        y = self.classifier(f)
        
        if self.loss == {'xent'}:
            return y
        elif self.loss == {'xent', 'htri'}:
            return y, f
        elif self.loss == {'cent'}:
            return y, f
        elif self.loss == {'ring'}:
            return y, f
        else:
            raise KeyError("Unsupported loss: {}".format(self.loss))

class DenseNet121_full(nn.Module):
    def __init__(self, num_classes, loss={'xent'}, **kwargs):
        super(DenseNet121_full, self).__init__()
        self.loss = loss
        densenet121 = torchvision.models.densenet121(pretrained=True)
        self.base0 = densenet121.features[0]
        self.base1 = densenet121.features[1]
        self.base2 = densenet121.features[2]
        self.base3 = densenet121.features[3]
        self.base4 = densenet121.features[4]#dense block
        self.base5 = densenet121.features[5]#composite function
        self.base6 = densenet121.features[6]#dense block
        self.base7 = densenet121.features[7]#composite function
        self.base8 = densenet121.features[8]#dense block
        self.base9 = densenet121.features[9]#composite function
        self.base10 = densenet121.features[10]#dense block
        self.base11 = densenet121.features[11]#batch normalization
        
        self.classifier = nn.Linear(1280, num_classes)
        self.feat_dim = 1280 # feature dimension
        self.use_salience = False
        self.use_parsing = False

    def forward(self, x):

        x = self.base0(x)
        x = self.base1(x)
        x = self.base2(x)
        x = self.base3(x)
        x = self.base4(x)
        x = self.base5(x)
        x = self.base6(x)
        x7= self.base7(x)#size = 256, 16, 8
        x = self.base8(x7)
        x = self.base9(x)
        x = self.base10(x)
        x = self.base11(x)

        x = F.avg_pool2d(x, x.size()[2:])
        x = x.view(x.size(0), -1)
        
        #use f7 as feature
        x7_feat = F.avg_pool2d(x7, x7.size()[2:]).view(x7.size()[:2])

        f = torch.cat((x, x7_feat), dim = 1)

        if not self.training:
            return f
        y = self.classifier(f)
        
        if self.loss == {'xent'}:
            return y
        elif self.loss == {'xent', 'htri'}:
            return y, f
        elif self.loss == {'cent'}:
            return y, f
        elif self.loss == {'ring'}:
            return y, f
        else:
            raise KeyError("Unsupported loss: {}".format(self.loss))
