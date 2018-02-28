package com.paperse.acagraph.Services;

import com.paperse.acagraph.Datemodels.Dto.UserinfoDTO;
import com.paperse.acagraph.Datemodels.Parameter.UserModifyParameter;
import com.paperse.acagraph.Datemodels.domain.Paper;
import com.paperse.acagraph.Datemodels.domain.QUserStats;
import com.paperse.acagraph.Utils.Constrain;
import com.querydsl.core.types.dsl.BooleanExpression;
import com.tagooo.op.Datemodels.Dto.RegCountDTO;
import com.tagooo.op.Datemodels.Dto.UserModifyDTO;
import com.tagooo.op.Datemodels.Dto.UserRemoveDTO;
import com.tagooo.op.Datemodels.domain.*;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by sunhaoran on 2017/7/24.
 */
@Service
public class UserService extends BaseService{

    public List<RegCountDTO> UserRegCount(String start_time, String end_time){
        if(start_time.equals("") || end_time.equals("") || start_time.compareTo(end_time) > 0){
            return new ArrayList<>();
        }

        QUserStats qUserStats = QUserStats.userStats;
        BooleanExpression p1 = qUserStats.regDate.between(start_time, end_time);
        BooleanExpression p2 = qUserStats.regDate.eq(start_time);
        BooleanExpression p3 = qUserStats.regDate.eq(end_time);
        List<UserStats> results = (List<UserStats>) userStatsDao.findAll(p1.or(p2.or(p3)), new Sort(Sort.Direction.ASC, "regDate"));
        if(results == null)
            return new ArrayList<>();
        List<RegCountDTO> regCountDTOS = new ArrayList<>();
        for(UserStats us : results){
            regCountDTOS.add(new RegCountDTO(us.getRegDate(), us.getCount()));
        }
        return regCountDTOS;
    }

    public void UserRegStat1Day(String date){
        UserStats userStats = userStatsDao.findByRegDate(date);
        if(userStats != null)
            return;
        List<Paper> tangoUsers = tangoUserDao.findByRegDateAndValid(date, true);
        if(tangoUsers == null)
            tangoUsers = new ArrayList<>();
        userStats = new UserStats();
        userStats.setCount(tangoUsers.size());
        userStats.setRegDate(date);
        userStatsDao.save(userStats);
    }

    public List<UserinfoDTO> FindAll(){
        List<Paper> tangoUsers = tangoUserDao.findByValid(true);
        List<UserinfoDTO> userinfoDTOS = new ArrayList<>();
        for(Paper u : tangoUsers){
            userinfoDTOS.add(new UserinfoDTO(u));
        }
        return userinfoDTOS;
    }

    @Transactional
    public UserRemoveDTO Remove(String userid){
        Paper tangoUser = tangoUserDao.findByIdAndValid(userid, true);
        if(tangoUser == null){
            logger.info("该用户不存在");
            return new UserRemoveDTO(1);
        }
        List<User2Service> user2Services = user2ServiceDao.findByUserIdAndValid(userid, true);
        if(user2Services != null) {
            for(User2Service u : user2Services){
                u.setValid(false);
                user2ServiceDao.save(u);
            }
        }
        List<TangoService> tangoServices = tangoServiceDao.findByPublishUserIdAndValid(userid, true);
        for(TangoService t : tangoServices){
            List<User2Service> user2Services1 = user2ServiceDao.findByServiceIdAndValid(t.getId(),true);
            for(User2Service u : user2Services1){
                u.setValid(false);
                user2ServiceDao.save(u);
            }
            List<Service2Picture> service2Pictures = service2PictureDao.findByServiceIdAndValid(t.getId(), true);
            for(Service2Picture s : service2Pictures){
                s.setValid(false);
                service2PictureDao.save(s);
            }
            t.setValid(false);
            tangoServiceDao.save(t);
        }
        tangoUser.setValid(false);
        tangoUserDao.save(tangoUser);
        return new UserRemoveDTO(0);
    }

    @Transactional
    public UserModifyDTO Modify(UserModifyParameter userModifyParameter){
        Paper tangoUser = tangoUserDao.findByIdAndValid(userModifyParameter.getId(), true);
        if(tangoUser == null){
            logger.info("该用户不存在");
            return new UserModifyDTO(1);
        }
        Boolean flag = tangoUser.getAddress().equals(userModifyParameter.getAddress());
        tangoUser.setInfo(userModifyParameter);
        tangoUserDao.save(tangoUser);
        if(!flag){
            RefreshDistance(tangoUser);
        }
        return new UserModifyDTO(0);
    }

    private void RefreshDistance(Paper tangoUser){
        List<TangoService> tangoServices = tangoServiceDao.findByPublishUserIdAndValid(tangoUser.getId(), true);
        for (TangoService tangoService : tangoServices){
            List<User2Service> user2Services = user2ServiceDao.findByServiceIdAndValid(tangoService.getId(), true);
            for (User2Service user2Service : user2Services) {
                Double distance = Constrain.getDistance(user2Service.getLongitude(), user2Service.getLatitude(), tangoUser.getLongitude(), tangoUser.getLatitude());
                user2Service.setDistance(distance);
                user2ServiceDao.save(user2Service);
            }
        }
    }
}
