package com.paperse.acagraph.Services;

import org.springframework.stereotype.Service;

/**
 * Created by sunhaoran on 2017/7/24.
 */
@Service
public class UserService extends BaseService{

//    @Transactional
//    public UserModifyDTO Modify(UserModifyParameter userModifyParameter){
//        Paper tangoUser = tangoUserDao.findByIdAndValid(userModifyParameter.getId(), true);
//        if(tangoUser == null){
//            logger.info("该用户不存在");
//            return new UserModifyDTO(1);
//        }
//        Boolean flag = tangoUser.getAddress().equals(userModifyParameter.getAddress());
//        tangoUser.setInfo(userModifyParameter);
//        tangoUserDao.save(tangoUser);
//        if(!flag){
//            RefreshDistance(tangoUser);
//        }
//        return new UserModifyDTO(0);
//    }
}
