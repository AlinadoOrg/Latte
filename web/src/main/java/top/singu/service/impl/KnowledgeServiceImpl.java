package top.singu.service.impl;

import org.springframework.stereotype.Service;
import top.singu.entity.TextContext;
import top.singu.knowledge.KnowledgeRepertory;
import top.singu.service.IKnowledgeService;

import javax.annotation.Resource;

@Service
public class KnowledgeServiceImpl implements IKnowledgeService{
	
	@Resource( name = "knowledgeRepertory" )
	private KnowledgeRepertory knowledgeRepertory;
	
	@Override
	public TextContext knowledgeAcquisition( String question ) {
		return knowledgeRepertory.knowledgeAcquisition( "turing", question );
	}
}
