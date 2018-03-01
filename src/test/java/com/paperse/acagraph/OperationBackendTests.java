package com.paperse.acagraph;

import com.paperse.acagraph.Datemodels.Dao.PaperDao;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import org.springframework.test.context.web.WebAppConfiguration;

/**
 * Created by sunhaoran on 2017/8/8.
 */
@RunWith(SpringJUnit4ClassRunner.class)
@SpringBootTest(classes = PaperseReadinApplication.class)
@WebAppConfiguration
//@ComponentScan(basePackages = {"com.tagooo.op.Datemodels.Dao"})
//@Component
public class OperationBackendTests {

    @Autowired
    private PaperDao paperDao;

    @Test
    //@Transactional
    public void TransactionTest(){
//        Paper tangoUser = new Paper();
//        tangoUser.setValid(true);
//        tangoUserDao.save(tangoUser);
//        //Paper tangoUser1 = tangoUserDao.findByIdAndValid("aaa", true);
//        //tangoUser1.setValid(false);
    }
}
