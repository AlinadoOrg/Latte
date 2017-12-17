package top.singu.service;

import top.singu.entity.TextContext;

/**
 * Created by singu on 17-10-31.
 */
public interface IKnowledgeService {

	TextContext knowledgeAcquisition( String question );
}
