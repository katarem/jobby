from constant.card_variables import CardVariables
from constant.languages import Languages
from model.config import Config
from model.job import Job
from model.search_result import SearchResult


class InjectorService:

    def inject_variables(self, config: Config, result: SearchResult) -> str:
        final_content = config.card_template
        for variable in CardVariables:
            if variable.value in config.card_template:
                final_content = self.resolve_variable(config,result,final_content, variable)
        return final_content

    def resolve_variable(self, config: Config, result: SearchResult, content: str, variable: CardVariables) -> str:
        replacement_info = ''
        if variable == CardVariables.JOB_TITLE:
            replacement_info = result.job.title
        if variable == CardVariables.COMPANY_NAME:
            replacement_info = result.job.business
        if variable == CardVariables.NAME:
            replacement_info = config.card_name
        if variable == CardVariables.PLATFORM:
            replacement_info = 'LinkedIn' # For the moment the only one we give support
        if variable == CardVariables.SKILLS_LIST:
            replacement_info = self.resolve_skills_list(result.matching_keywords, config.card_language)
        return content.replace(variable.value, replacement_info)
    
    def resolve_skills_list(self, skills_list: list[str], language: str) -> str:
        skills = ''
        if not skills_list:  # Handle empty list case
            return skills  # Return an empty string if no skills are provided
        if len(skills_list) < 2:
            return skills_list[0].capitalize()
        skills = ', '.join(skill.capitalize() for skill in skills_list[:-1])
        if language == Languages.ENGLISH.value:
            last_connector = ' and '
        if language == Languages.SPANISH.value:
            last_connector = ' y '
        skills += last_connector + skills_list[-1].capitalize()
        return skills
