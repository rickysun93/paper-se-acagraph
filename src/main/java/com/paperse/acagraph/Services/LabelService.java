package com.paperse.acagraph.Services;

import com.tagooo.op.Datemodels.domain.BasicLabel;
import com.tagooo.op.Datemodels.domain.ServiceLabel;
import com.tagooo.op.Datemodels.domain.TangoService;
import com.tagooo.op.Datemodels.domain.ThirdLabel;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * Created by sunhaoran on 2017/7/19.
 */
@Service
public class LabelService extends BaseService{

    public String AddThirdLabel(String label, String serviceLabelId) {
        if (label.equals("")) {
            logger.info("三级标签为空");
            return "{\"result\":\"error:三级标签为空\"}";
        }
        ThirdLabel thirdLabel = thirdLabelDao.findByServiceTypeIdAndTypeAndValid(serviceLabelId, label, true);
        if (thirdLabel != null) {
            logger.info("该二级标签下三级标签已存在");
            return "{\"result\":\"error:三级标签已存在\"}";
        }
        ServiceLabel serviceLabel = serviceLabelDao.findByIdAndValid(serviceLabelId, true);
        if (serviceLabel == null) {
            logger.info("二级服务标签不存在");
            return "{\"result\":\"error:对应的二级服务标签不存在\"}";
        }
        thirdLabel = new ThirdLabel();
        thirdLabel.setInfo(label, serviceLabelId);
        thirdLabelDao.save(thirdLabel);
        return "{\"result\":\"OK\"}";
    }

    public String RemoveThirdLabel(String id) {
        ThirdLabel thirdLabel = thirdLabelDao.findByIdAndValid(id, true);
        if (thirdLabel == null) {
            logger.info("该label不存在");
            return "{\"result\":\"error:三级标签不存在\"}";
        }
        List<TangoService> tangoServices = tangoServiceDao.findByThirdLabelIdAndValid(id, true);
        if(tangoServices.size() > 0){
            logger.info("该标签有依赖服务");
            return "{\"result\":\"error:该标签有依赖服务\"}";
        }
        thirdLabel.setValid(false);
        thirdLabelDao.save(thirdLabel);
        return "{\"result\":\"OK\"}";
    }

    public String AddServiceLabel(String label, String basicLabelId) {
        if (label.equals("")) {
            logger.info("服务标签为空");
            return "{\"result\":\"error:服务标签为空\"}";
        }
        ServiceLabel serviceLabel = serviceLabelDao.findByTypeAndValid(label, true);
        if (serviceLabel != null) {
            logger.info("该服务标签已存在");
            return "{\"result\":\"error:服务标签已存在\"}";
        }
        BasicLabel basicLabel = basicLabelDao.findByIdAndValid(basicLabelId, true);
        if (basicLabel == null) {
            logger.info("基础服务标签不存在");
            return "{\"result\":\"error:对应的基础服务标签不存在\"}";
        }
        serviceLabel = new ServiceLabel();
        serviceLabel.setInfo(label, basicLabelId);
        serviceLabelDao.save(serviceLabel);
        return "{\"result\":\"OK\"}";
    }

    public String RemoveServiceLabel(String id) {
        ServiceLabel serviceLabel = serviceLabelDao.findByIdAndValid(id, true);
        if (serviceLabel == null) {
            logger.info("该label不存在");
            return "{\"result\":\"error:二级服务标签不存在\"}";
        }
        List<ThirdLabel> thirdLabels = thirdLabelDao.findByServiceTypeIdAndValid(id, true);
        if(thirdLabels.size() > 0){
            logger.info("该标签有依赖label");
            return "{\"result\":\"error:该标签有依赖label\"}";
        }
        serviceLabel.setValid(false);
        serviceLabelDao.save(serviceLabel);
        return "{\"result\":\"OK\"}";
    }

    public String AddBasicLabel(String label) {
        if (label.equals("")) {
            logger.info("服务标签为空");
            return "{\"result\":\"error:服务标签为空\"}";
        }
        BasicLabel basicLabel = basicLabelDao.findByTypeAndValid(label, true);
        if (basicLabel != null) {
            logger.info("该服务标签已存在");
            return "{\"result\":\"error:服务标签已存在\"}";
        }
        basicLabel = new BasicLabel();
        basicLabel.setInfo(label);
        basicLabelDao.save(basicLabel);
        return "{\"result\":\"OK\"}";
    }

    public String RemoveBasicLabel(String id) {
        BasicLabel basicLabel = basicLabelDao.findByIdAndValid(id, true);
        if (basicLabel == null) {
            logger.info("该基础标签不存在");
            return "{\"result\":\"error:服务标签不存在\"}";
        }
        List<ServiceLabel> serviceLabels = serviceLabelDao.findByBasicTypeIdAndValid(id, true);
        if(serviceLabels.size() > 0){
            logger.info("该基础标签有依赖label");
            return "{\"result\":\"error:该基础标签有依赖label\"}";
        }
        basicLabel.setValid(false);
        basicLabelDao.save(basicLabel);
        return "{\"result\":\"OK\"}";
    }
}
