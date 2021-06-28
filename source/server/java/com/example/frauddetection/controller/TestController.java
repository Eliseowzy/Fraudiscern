package com.example.frauddetection.controller;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

import java.util.Map;


@RestController
public class TestController {
    Logger logger = LoggerFactory.getLogger(getClass());

    @RequestMapping("/hello")
    public String hello(){
        logger.info("请求测试");
        return "Hello Spring!";

    }

    @Autowired
    private KafkaTemplate<Object, Object> template;
    @GetMapping("/send/{input}")
    public void sendFoo(@PathVariable String input) {
        this.template.send("test", input);
    }
    @KafkaListener(id = "webGroup", topics = "test")
    public void listen(String input) {
        logger.info("input value: {}" , input);
    }

    @Controller
    @RequestMapping("/user")
    public class UserAction {
        @ResponseBody
        public String updateAttr(@RequestBody Map<String, Object> user) {
            //打印user
            logger.info(user.toString());
            return "success";
        }
    }

}
