package com.paperse.acagraph.Controllers;

import com.paperse.acagraph.Services.LabelService;
import com.paperse.acagraph.Services.ServiceService;
import com.paperse.acagraph.Services.UserService;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;

/**
 * Created by sunhaoran on 2017/7/19.
 */
public class BaseController {
    @Autowired
    protected LabelService labelService;

    @Autowired
    protected UserService userService;

    @Autowired
    protected ServiceService serviceService;

    protected static final Logger logger = LogManager.getLogger(BaseController.class);
}
