package top.singu.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.ModelAndView;
import top.singu.entity.Data;
import top.singu.entity.TextContext;
import top.singu.service.IKnowledgeService;

@RestController
@RequestMapping( "/api" )
public class ApiController {

	@Autowired
	private IKnowledgeService knowledgeService;
	
	@ResponseBody
	@RequestMapping( value = "/say/{context}", method = RequestMethod.GET )
	public Data ack(
			@PathVariable( "context" ) String context ){
		Data data = new Data( );
		TextContext textContext = knowledgeService.knowledgeAcquisition( context );
		data.setStatus( true );
		data.setCode( 200 );
		data.setData( textContext );
		data.setDataType( textContext.dataType );
		return data;
	}
}
