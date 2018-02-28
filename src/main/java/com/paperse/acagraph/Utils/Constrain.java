package com.paperse.acagraph.Utils;

/**
 * Created by sunhaoran on 2018/1/27.
 */
public class Constrain {
    public static Double getDistance(Double sLng, Double sLat, Double dLng, Double dLat) {
        Double pk = Math.PI / 180;
        Double a = sLng * pk;
        Double b = dLng * pk;
        Double c = sLat * pk;
        Double d = dLat * pk;
        Double dis = 6370996.81 * Math.acos(Math.sin(c) * Math.sin(d) + Math.cos(c) * Math.cos(d) * Math.cos(b - a));
        return dis / 1000;
    }
}
