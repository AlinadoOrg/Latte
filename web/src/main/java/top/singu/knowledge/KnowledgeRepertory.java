package top.singu.knowledge;

import top.singu.entity.TextContext;

import java.util.Map;

public class KnowledgeRepertory {
	
	private Map< String, Knowledge > knowledgeMap;
	
	public TextContext knowledgeAcquisition( String knowledgeName, String question ){
		Knowledge knowledge = knowledgeMap.get( knowledgeName );
		if( knowledge != null ){
			return knowledge.acquisition( question );
		}
		return new TextContext( "抱歉，我无法理解你说的话..." );
	}
	
	public Map< String, Knowledge > getKnowledgeMap( ) {
		return knowledgeMap;
	}
	
	public void setKnowledgeMap( Map< String, Knowledge > knowledgeMap ) {
		this.knowledgeMap = knowledgeMap;
	}
}
