package com.paperse.acagraph.Controllers;

import com.paperse.acagraph.Datemodels.Dto.UserinfoDTO;
import com.paperse.acagraph.Datemodels.Parameter.UserModifyParameter;
import com.tagooo.op.Datemodels.Dto.RegCountDTO;
import com.tagooo.op.Datemodels.Dto.UserModifyDTO;
import com.tagooo.op.Datemodels.Dto.UserRemoveDTO;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * Created by sunhaoran on 2017/7/24.
 */
@CrossOrigin
@RestController
public class UserController extends BaseController{
    @RequestMapping(value = "/user/regcount", method = RequestMethod.GET)
    public
    @ResponseBody
    List<RegCountDTO> UserRegCount(String start, String end) {
        return userService.UserRegCount(start, end);
    }

    @RequestMapping(value = "/user/test", method = RequestMethod.GET)
    public
    @ResponseBody
    void test(String date) {
        userService.UserRegStat1Day(date);
    }

    @RequestMapping(value = "/user/findall", method = RequestMethod.GET)
    public
    @ResponseBody
    List<UserinfoDTO> FindAll(){
        return userService.FindAll();
    }

    @RequestMapping(value = "/user/remove", method = RequestMethod.GET)
    public
    @ResponseBody
    UserRemoveDTO Remove(String userid){
        return userService.Remove(userid);
    }

    @RequestMapping(value = "/user/modify", method = RequestMethod.POST)
    public
    @ResponseBody
    UserModifyDTO Modify(@RequestBody UserModifyParameter userModifyParameter){
        return userService.Modify(userModifyParameter);
    }
}
