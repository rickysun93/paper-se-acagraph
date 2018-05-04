package com.paperse.acagraph.Controllers;

import org.springframework.web.bind.annotation.*;

/**
 * Created by sunhaoran on 2017/7/24.
 */
@CrossOrigin
@RestController
public class TsetController extends BaseController{
//    @RequestMapping(value = "/user/findall", method = RequestMethod.GET)
//    public
//    @ResponseBody
//    List<UserinfoDTO> FindAll(){
//        return userService.FindAll();
//    }

    @RequestMapping(value = "/test/readin", method = RequestMethod.GET)
    public
    @ResponseBody
    String Readin(){
        return testService.Readin();
    }

    @RequestMapping(value = "/test/graph", method = RequestMethod.GET)
    public
    @ResponseBody
    String Graph(){
        return testService.Graph();
    }
}
