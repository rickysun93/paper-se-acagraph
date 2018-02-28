package com.paperse.acagraph.Utils;


import com.paperse.acagraph.Services.ServiceService;
import com.paperse.acagraph.Services.UserService;
import org.apache.log4j.LogManager;
import org.apache.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.text.SimpleDateFormat;
import java.util.Calendar;

/**
 * Created by sunhaoran on 2017/7/28.
 */
@Component
public class Stats {
    private static final Logger logger = LogManager.getLogger(Stats.class);

    @Autowired
    private UserService userService;
    @Autowired
    private ServiceService serviceService;

    @Scheduled(cron="0 0 1 * * ?")
    public void run(){
        Calendar cal = Calendar.getInstance();
        cal.add(Calendar.DATE, -1);
        String date = new SimpleDateFormat("yyyyMMdd").format(cal.getTime());
        userService.UserRegStat1Day(date);
        serviceService.ServiceRegStat1Day(date);
    }
}
