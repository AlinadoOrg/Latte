package top.singu.knowledge.impl;

import com.fasterxml.jackson.databind.ObjectMapper;
import top.singu.entity.TextContext;
import top.singu.entity.TuringJson;
import top.singu.knowledge.Knowledge;
import top.singu.utils.HttpClient;

import javax.annotation.Resource;
import java.io.IOException;

public class TuringRobotKnowledge implements Knowledge{
	
	@Resource( name = "objectMapper" )
	private ObjectMapper mapper;
	
	private String apiurl;
	private String apikey;
	
	@Override
	public TextContext acquisition( String question ) {
		TextContext textContext = new TextContext( );
		try {
			StringBuffer param = new StringBuffer( );
			param.append( "key=" ).append( apikey );
			param.append( "&info=" ).append( question );
			param.append( "&userid=12345" );
			String json = HttpClient.sendPost( apiurl, param.toString( ) );
			TuringJson turingJson = mapper.readValue( json, TuringJson.class );
			textContext.setContext( turingJson.getText( ) );
		} catch ( IOException e ) {
			e.printStackTrace( );
		}
		return textContext;
	}
	
	public void setApiurl( String apiurl ) {
		this.apiurl = apiurl;
	}
	
	public void setApikey( String apikey ) {
		this.apikey = apikey;
	}
	
}
