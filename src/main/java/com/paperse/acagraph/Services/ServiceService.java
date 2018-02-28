package com.paperse.acagraph.Services;

import com.paperse.acagraph.Datemodels.domain.QServiceStats;
import com.querydsl.core.types.dsl.BooleanExpression;
import com.tagooo.op.Datemodels.Dto.RegCountDTO;
import com.tagooo.op.Datemodels.Dto.ServiceModifyDTO;
import com.tagooo.op.Datemodels.Dto.ServiceRemoveDTO;
import com.tagooo.op.Datemodels.Dto.ServiceinfoDTO;
import com.tagooo.op.Datemodels.Parameter.ServiceModifyParameter;
import com.tagooo.op.Datemodels.domain.*;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by sunhaoran on 2017/7/27.
 */
@Service
public class ServiceService extends BaseService {

    public List<RegCountDTO> ServiceRegCount(String start_time, String end_time){
        if(start_time.equals("") || end_time.equals("") || start_time.compareTo(end_time) > 0){
            return new ArrayList<>();
        }

        QServiceStats qServiceStats = QServiceStats.serviceStats;
        BooleanExpression p1 = qServiceStats.regDate.between(start_time, end_time);
        BooleanExpression p2 = qServiceStats.regDate.eq(start_time);
        BooleanExpression p3 = qServiceStats.regDate.eq(end_time);
        List<ServiceStats> results = (List<ServiceStats>) serviceStatsDao.findAll(p1.or(p2.or(p3)), new Sort(Sort.Direction.ASC, "regDate"));
        if(results == null)
            return new ArrayList<>();
        List<RegCountDTO> regCountDTOS = new ArrayList<>();
        for(ServiceStats ss : results){
            regCountDTOS.add(new RegCountDTO(ss.getRegDate(), ss.getCount()));
        }
        return regCountDTOS;
    }

    public void ServiceRegStat1Day(String date){
        ServiceStats serviceStats = serviceStatsDao.findByRegDate(date);
        if(serviceStats != null)
            return;
        List<TangoService> tangoServices = tangoServiceDao.findByDatetimeAndValid(date, true);
        if(tangoServices == null)
            tangoServices = new ArrayList<>();
        serviceStats = new ServiceStats();
        serviceStats.setCount(tangoServices.size());
        serviceStats.setRegDate(date);
        serviceStatsDao.save(serviceStats);
    }

    public List<ServiceinfoDTO> FindAll(){
        List<TangoService> tangoServices = tangoServiceDao.findByValid(true);
        List<ServiceinfoDTO> serviceinfoDTOS = new ArrayList<>();
        for(TangoService s : tangoServices){
            ThirdLabel thirdLabel = thirdLabelDao.findByIdAndValid(s.getThirdLabelId(), true);
            ServiceLabel serviceLabel = serviceLabelDao.findByIdAndValid(thirdLabel.getServiceTypeId(), true);
            BasicLabel basicLabel = basicLabelDao.findByIdAndValid(serviceLabel.getBasicTypeId(), true);
            serviceinfoDTOS.add(new ServiceinfoDTO(s, basicLabel, serviceLabel, thirdLabel));
        }
        return serviceinfoDTOS;
    }

    @Transactional
    public ServiceRemoveDTO Remove(String serviceid){
        TangoService tangoService = tangoServiceDao.findByIdAndValid(serviceid, true);
        if(tangoService == null){
            logger.info("该服务不存在");
            return new ServiceRemoveDTO(1);
        }
        List<User2Service> user2Services = user2ServiceDao.findByServiceIdAndValid(serviceid, true);
        for(User2Service u : user2Services){
            u.setValid(false);
            user2ServiceDao.save(u);
        }
        List<Service2Picture> service2Pictures = service2PictureDao.findByServiceIdAndValid(serviceid, true);
        for(Service2Picture s : service2Pictures){
            s.setValid(false);
            service2PictureDao.save(s);
        }
        tangoService.setValid(false);
        tangoServiceDao.save(tangoService);
        return new ServiceRemoveDTO(0);
    }

    public ServiceModifyDTO Modify(ServiceModifyParameter serviceModifyParameter){
        TangoService tangoService = tangoServiceDao.findByIdAndValid(serviceModifyParameter.getId(), true);
        if(tangoService == null){
            logger.info("该服务不存在");
            return new ServiceModifyDTO(1);
        }
        tangoService.setInfo(serviceModifyParameter);
        tangoServiceDao.save(tangoService);
        return new ServiceModifyDTO(0);
    }
}
