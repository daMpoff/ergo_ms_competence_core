export const competenceCoreEndpoints = {
  competenceCore: {
    // Компетенции
    competencesList: 'competence_core/competences/',
    competenceDetail: (id) => `competence_core/competences/${id}/`,

    // Профили вакансий
    vacancyProfilesList: 'competence_core/vacancy-profiles/',
    vacancyProfileDetail: (id) => `competence_core/vacancy-profiles/${id}/`,
    vacancyProfileCompetences: (id) => `competence_core/vacancy-profiles/${id}/competences/`,

    // Технологии (skill_map)
    technologiesList: 'competence_core/skill-map/technologies/',
    technologyCategories: 'competence_core/skill-map/technologies/categories/',
    technologyAliases: (id) => `competence_core/skill-map/technologies/${id}/aliases/`,
    technologyChildren: (id) => `competence_core/skill-map/technologies/${id}/children/`,
  },
}


