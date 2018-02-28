package com.paperse.acagraph.Controllers;

import com.tagooo.op.Datemodels.Dto.RegCountDTO;
import com.tagooo.op.Datemodels.Dto.ServiceModifyDTO;
import com.tagooo.op.Datemodels.Dto.ServiceRemoveDTO;
import com.tagooo.op.Datemodels.Dto.ServiceinfoDTO;
import com.tagooo.op.Datemodels.Parameter.ServiceModifyParameter;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * Created by sunhaoran on 2017/7/27.
 */
@CrossOrigin
@RestController
public class ServiceController extends BaseController {
    @RequestMapping(value = "/service/regcount", method = RequestMethod.GET)
    public
    @ResponseBody
    List<RegCountDTO> ServiceRegCount(String start, String end) {
        return serviceService.ServiceRegCount(start, end);
    }

    @RequestMapping(value = "/service/test", method = RequestMethod.GET)
    public
    @ResponseBody
    void test(String date) {
        serviceService.ServiceRegStat1Day(date);
    }

    @RequestMapping(value = "/service/findall", method = RequestMethod.GET)
    public
    @ResponseBody
    List<ServiceinfoDTO> FindAll(){
        return serviceService.FindAll();
    }

    @RequestMapping(value = "/service/remove", method = RequestMethod.GET)
    public
    @ResponseBody
    ServiceRemoveDTO Remove(String serviceid){
        return serviceService.Remove(serviceid);
    }

    @RequestMapping(value = "/service/modify", method = RequestMethod.POST)
    public
    @ResponseBody
    ServiceModifyDTO Modify(@RequestBody ServiceModifyParameter serviceModifyParameter){
        return serviceService.Modify(serviceModifyParameter);
    }
}
