package com.paperse.acagraph.Controllers;

import org.springframework.web.bind.annotation.*;

/**
 * Created by sunhaoran on 2017/7/19.
 */
@CrossOrigin
@RestController
public class LabelController extends BaseController{

    @RequestMapping(value = "/service/addthirdlabel", method = RequestMethod.GET)
    public
    @ResponseBody
    String AddThirdLabel(String label, String serviceLabelId) {
        return labelService.AddThirdLabel(label, serviceLabelId);
    }

    @RequestMapping(value = "/service/removethirdlabel", method = RequestMethod.GET)
    public
    @ResponseBody
    String RemoveThirdLabel(String id) {
        return labelService.RemoveThirdLabel(id);
    }

    @RequestMapping(value = "/service/addservicelabel", method = RequestMethod.GET)
    public
    @ResponseBody
    String AddServiceLabel(String label, String basicLabelId) {
        return labelService.AddServiceLabel(label, basicLabelId);
    }

    @RequestMapping(value = "/service/removeservicelabel", method = RequestMethod.GET)
    public
    @ResponseBody
    String RemoveServiceLabel(String id) {
        return labelService.RemoveServiceLabel(id);
    }

    @RequestMapping(value = "/service/addbasiclabel", method = RequestMethod.GET)
    public
    @ResponseBody
    String AddBasicLabel(String label) {
        return labelService.AddBasicLabel(label);
    }

    @RequestMapping(value = "/service/removebasiclabel", method = RequestMethod.GET)
    public
    @ResponseBody
    String RemoveBasicLabel(String id) {
        return labelService.RemoveBasicLabel(id);
    }

}
